# RAG Chatbot - Modern Web Interface

This is a RAG (Retrieval Augmented Generation) chatbot with a modern web interface featuring user authentication and document-based Q&A.

## Features

- ✅ User Registration & Login System
- ✅ PDF Document Upload (Multiple files supported)
- ✅ Drag & Drop File Upload
- ✅ Real-time Chat Interface
- ✅ RAG-based Question Answering
- ✅ Modern, Responsive UI
- ✅ Chat History Persistence
- ✅ Vector Database (Chroma) for document embeddings

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app_flask.py
```

The application will start on `http://localhost:5000`

### 3. Access the Application

- Open your browser and navigate to `http://localhost:5000`
- You'll see the login page

## Usage Guide

### First Time Setup

1. **Register an Account**
   - Click "Register here" on the login page
   - Fill in your username, email, and password
   - Click "Register"
   - You'll be redirected to the login page

2. **Login**
   - Enter your username and password
   - Click "Login"
   - You'll be redirected to the chat interface

### Using the Chat Interface

1. **Upload PDFs**
   - Click "Browse Files" or drag & drop PDF files into the upload area
   - Multiple PDFs can be uploaded at once
   - Wait for the processing to complete
   - Uploaded files will appear in the sidebar

2. **Ask Questions**
   - Once PDFs are uploaded, the chat input will be enabled
   - Type your question in the input box
   - Press Enter or click "Send"
   - The AI will respond based on the content of your uploaded PDFs

3. **Chat Features**
   - Questions are answered using context from your uploaded PDFs
   - The AI cites the filename and page number for each answer
   - Chat history is maintained during your session
   - Loading indicators show when the AI is thinking

4. **Logout**
   - Click the "Logout" button in the sidebar to end your session

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: Google Gemini 2.0 Flash
- **Vector Database**: ChromaDB
- **Embeddings**: HuggingFace Sentence Transformers
- **PDF Processing**: pypdf
- **Authentication**: Flask Sessions with Werkzeug password hashing

## File Structure

```
RAG-Chatbot-main/
├── app_flask.py          # Flask backend server
├── brain.py              # RAG logic and PDF processing
├── requirements.txt      # Python dependencies
├── users.json           # User data storage (auto-created)
├── chroma_db/           # Vector database storage
├── uploads/             # Temporary PDF storage (auto-created)
└── frontend/
    ├── login.html       # Login page
    ├── register.html    # Registration page
    ├── chat.html        # Chat interface
    ├── style.css        # Styling
    ├── login.js         # Login functionality
    ├── register.js      # Registration functionality
    └── chat.js          # Chat functionality
```

## Security Notes

⚠️ **Important for Production:**

1. Change the `app.secret_key` in [app_flask.py](app_flask.py)
2. Move the Gemini API key to environment variables
3. Use a proper database instead of JSON file for user storage
4. Implement HTTPS
5. Add rate limiting
6. Add input validation and sanitization

## Original Streamlit Version

The original Streamlit version is preserved in [app.py](app.py). You can still run it with:

```bash
streamlit run app.py
```

## Troubleshooting

**Issue**: ModuleNotFoundError
- **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Port already in use
- **Solution**: Change the port in [app_flask.py](app_flask.py) (line 262): `app.run(debug=True, port=5001)`

**Issue**: PDFs not processing
- **Solution**: Ensure the PDFs are not corrupted and are actual PDF files

**Issue**: Chat input disabled
- **Solution**: Upload at least one PDF first

## Support

For issues or questions, please check the code comments in the respective files or modify as needed for your use case.

---

Built with ❤️ using Flask, Google Gemini, and ChromaDB
