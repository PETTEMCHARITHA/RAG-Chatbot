from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

# Disable ChromaDB telemetry to prevent errors
os.environ["ANONYMIZED_TELEMETRY"] = "False"
from datetime import datetime, timedelta
from brain import get_index_for_pdf
import google.generativeai as genai
import config
import uuid
import glob
from io import BytesIO

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Enable CORS properly
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Auth-Token"]
    }
})

# Set up the Gemini API key
GEMINI_API_KEY = config.GEMINI_API_KEY
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Documents folder configuration
DOCUMENTS_FOLDER = 'documents'
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

# User data storage
USERS_FILE = 'users.json'
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

# Token-based authentication
auth_tokens = {}  # {token: {username, created_at}}
user_data = {}  # {username: {chat_history}}

# SHARED vector database for all users (loaded from documents folder)
shared_vectordb = None
loaded_documents = []

def load_documents_from_folder():
    """Load all PDFs from documents folder and create shared vector database"""
    global shared_vectordb, loaded_documents
    
    print("🔍 Scanning documents folder for PDFs...")
    pdf_files = glob.glob(os.path.join(DOCUMENTS_FOLDER, '*.pdf'))
    
    if not pdf_files:
        print("⚠️ No PDF files found in documents folder")
        return
    
    print(f"📚 Found {len(pdf_files)} PDF files")
    
    # Read all PDFs and combine them
    all_pdf_data = []
    all_pdf_names = []
    failed_files = []
    
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"  📄 Loading: {filename}")
        try:
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()
                all_pdf_data.append(pdf_bytes)
                all_pdf_names.append(filename)
            print(f"  ✅ Loaded: {filename} ({len(pdf_bytes)} bytes)")
        except Exception as e:
            print(f"  ❌ Error loading {filename}: {str(e)}")
            failed_files.append(filename)
    
    if not all_pdf_data:
        print("❌ No PDFs could be loaded")
        return
    
    # Process all PDFs using brain.py logic (handles individual PDF errors internally)
    print(f"\n🧠 Processing {len(all_pdf_data)} PDFs and creating vector database...")
    try:
        # Call get_index_for_pdf with the correct parameters
        shared_vectordb = get_index_for_pdf(
            all_pdf_data,
            all_pdf_names,
            GEMINI_API_KEY
        )
        
        # Update loaded_documents to reflect successfully parsed PDFs
        loaded_documents.clear()
        loaded_documents.extend(all_pdf_names)
        
        print(f"✅ Vector database created successfully!")
        print(f"📋 Loaded documents: {', '.join(loaded_documents)}")
        
    except Exception as e:
        print(f"❌ Error creating vector database: {str(e)}")
        print(f"   All PDFs failed to parse. Please check the PDF files.")

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def get_auth_token(request):
    """Extract auth token from request"""
    # Check Authorization header
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    
    # Check X-Auth-Token header
    token = request.headers.get('X-Auth-Token')
    if token:
        return token
    
    # Check query parameter (for debugging)
    token = request.args.get('token')
    if token:
        return token
    
    return None

def verify_token(token):
    """Verify auth token and return username"""
    if not token or token not in auth_tokens:
        return None
    
    # Check if token is expired (24 hours)
    token_data = auth_tokens[token]
    created = datetime.fromisoformat(token_data['created_at'])
    if datetime.now() - created > timedelta(hours=24):
        del auth_tokens[token]
        return None
    
    return token_data['username']

# Routes for serving HTML pages
@app.route('/')
def index():
    return send_from_directory('frontend', 'login.html')

@app.route('/register')
def register_page():
    return send_from_directory('frontend', 'register.html')

@app.route('/chat')
def chat_page():
    return send_from_directory('frontend', 'chat.html')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

# Authentication APIs
@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    
    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
    
    try:
        users = load_users()
        
        if username in users:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        users[username] = {
            'email': email,
            'password': generate_password_hash(password),
            'created_at': datetime.now().isoformat()
        }
        
        save_users(users)
        print(f"[REGISTER] New user registered: {username}")
        return jsonify({'success': True, 'message': 'Registration successful'}), 201
        
    except Exception as e:
        print(f"[REGISTER] Error: {str(e)}")
        return jsonify({'success': False, 'message': f'Registration error: {str(e)}'}), 500

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    
    print(f"[LOGIN] Login attempt for user: {username}")
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    try:
        users = load_users()
        
        if username not in users:
            print(f"[LOGIN] User not found: {username}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        user_stored = users[username]
        if not check_password_hash(user_stored['password'], password):
            print(f"[LOGIN] Invalid password for user: {username}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Create auth token
        token = str(uuid.uuid4())
        auth_tokens[token] = {
            'username': username,
            'created_at': datetime.now().isoformat()
        }
        
        # Initialize user data
        if username not in user_data:
            user_data[username] = {
                'chat_history': []
            }
        
        print(f"[LOGIN] User logged in successfully: {username}, token: {token[:10]}...")
        return jsonify({
            'success': True, 
            'message': 'Login successful',
            'token': token,
            'username': username
        }), 200
        
    except Exception as e:
        print(f"[LOGIN] Error: {str(e)}")
        return jsonify({'success': False, 'message': f'Login error: {str(e)}'}), 500

@app.route('/api/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return '', 204
    
    token = get_auth_token(request)
    if token and token in auth_tokens:
        username = auth_tokens[token]['username']
        del auth_tokens[token]
        if username in user_data:
            del user_data[username]
        print(f"[LOGOUT] User logged out: {username}")
    
    return jsonify({'success': True, 'message': 'Logout successful'}), 200

# Documents status API
@app.route('/api/documents-status', methods=['GET', 'OPTIONS'])
def documents_status():
    if request.method == 'OPTIONS':
        return '', 204
    
    return jsonify({
        'success': True,
        'documents_loaded': len(loaded_documents) > 0,
        'document_count': len(loaded_documents),
        'documents': loaded_documents
    }), 200

# Chat API
@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 204
    
    # Get and verify auth token
    token = get_auth_token(request)
    username = verify_token(token)
    
    if not username:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    print(f"[CHAT] Chat request from: {username}")
    
    # Check if shared documents are loaded
    if not shared_vectordb:
        return jsonify({'success': False, 'message': 'No documents loaded. Please add PDFs to the documents folder and restart the server.'}), 400
    
    data = request.get_json() or {}
    question = (data.get('question') or '').strip()
    
    if not question:
        return jsonify({'success': False, 'message': 'No question provided'}), 400
    
    try:
        # Initialize chat history if needed
        if username not in user_data:
            user_data[username] = {'chat_history': []}
        
        chat_history = user_data[username]['chat_history']
        
        # Search the shared vectordb
        search_results = shared_vectordb.similarity_search(question, k=3)
        pdf_extract = "\n ".join([result.page_content for result in search_results])
        
        prompt_template = """You are a helpful Assistant who answers to users questions based on multiple contexts given to you.
Keep your answer short and to the point.
The evidence are the context of the pdf extract with metadata.
Carefully focus on the metadata specially 'filename' and 'page' whenever answering.
Make sure to add filename and page number at the end of sentence you are citing to.
Reply "Not applicable" if text is irrelevant.

The PDF content is:
{pdf_extract}"""
        
        # Get response from Gemini
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        response_text = ""
        try:
            response = model.generate_content(question + "\n\nContext: " + pdf_extract)
            response_text = response.text
            print(f"[CHAT] Response generated for {username}")
        except Exception as e:
            response_text = f"I couldn't generate a response: {str(e)}"
            print(f"[CHAT] Gemini error: {str(e)}")
        
        # Add to history
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": response_text})
        user_data[username]['chat_history'] = chat_history
        
        return jsonify({
            'success': True,
            'response': response_text
        }), 200
        
    except Exception as e:
        print(f"[CHAT] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Chat error: {str(e)}'}), 500

# Get chat history
@app.route('/api/chat-history', methods=['GET', 'OPTIONS'])
def get_chat_history():
    if request.method == 'OPTIONS':
        return '', 204
    
    token = get_auth_token(request)
    username = verify_token(token)
    
    if not username:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    if username not in user_data:
        return jsonify({'success': True, 'history': []}), 200
    
    history = user_data[username]['chat_history']
    filtered_history = [msg for msg in history if msg['role'] != 'system']
    
    return jsonify({'success': True, 'history': filtered_history}), 200

if __name__ == '__main__':
    print(f"\n{'='*60}")
    print(f" Starting RAG Chatbot Server")
    print(f"{'='*60}\n")
    
    # Load documents from folder on startup
    load_documents_from_folder()
    
    print(f"\n{'='*60}")
    print(f" Server Configuration")
    print(f"{'='*60}")
    print(f" URL: http://{config.HOST}:{config.PORT}")
    print(f" Documents loaded: {len(loaded_documents)}")
    if loaded_documents:
        for doc in loaded_documents:
            print(f"   - {doc}")
    print(f" Press CTRL+C to stop")
    print(f"{'='*60}\n")
    
    app.run(debug=config.DEBUG, port=config.PORT, host=config.HOST, threaded=True)
