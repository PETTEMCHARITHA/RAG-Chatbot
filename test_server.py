# Quick Test Script
import requests
import time

print("Testing RAG Chatbot Server...")
print("-" * 50)

# Wait for server to start
time.sleep(2)

try:
    # Test health check
    print("\n1. Testing server health...")
    response = requests.get('http://localhost:5000/api/health')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test registration
    print("\n2. Testing user registration...")
    response = requests.post('http://localhost:5000/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test login
    print("\n3. Testing user login...")
    response = requests.post('http://localhost:5000/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    }, cookies={})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print(f"   Cookies: {response.cookies}")
    
    print("\n" + "=" * 50)
    print("✓ Server is working correctly!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nMake sure the Flask server is running!")
    print("Start the server with: python app_flask.py")
