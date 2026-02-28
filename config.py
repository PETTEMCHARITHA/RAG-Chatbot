# Configuration File
# Change these settings as needed

# Google Gemini API Key
# Get your key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyBM7Fd6nh5xLzdzbIO8kEoohYKvc6zhQEQ"

# Flask Secret Key (change this to a random string for production)
FLASK_SECRET_KEY = "your-secret-key-change-this-in-production-2024"

# Server Settings
DEBUG = True
PORT = 5000
HOST = "127.0.0.1"

# File Upload Settings
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
UPLOAD_FOLDER = 'uploads'

# Email Configuration (SMTP)
# ===========================
# For Gmail, use: smtp.gmail.com, port 587
# Generate app-specific password from: https://myaccount.google.com/apppasswords
# Note: 2-factor authentication must be enabled
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'charithapettem2532@gmail.com',
    'sender_password': 'mcmb dmju orlh aaej',
    'sender_name': 'RAG Chatbot'
}

# Email Settings
ENABLE_INSTANT_EMAILS = True      # Send email after each query
ENABLE_WEEKLY_DIGEST = True       # Send weekly digest emails
ENABLE_CONCEPT_UPDATES = True     # Send concept-based alerts

# Default Email Preferences for New Users
DEFAULT_EMAIL_PREFERENCES = {
    'instant_notification': False,   # Don't notify on every query (can be spammy)
    'weekly_digest': True,           # Enable weekly digest by default
    'concept_updates': True,         # Enable concept updates by default
    'new_document_alerts': True,     # Alert when new docs match interests
    'frequency': 'weekly'            # Options: 'immediate', 'weekly', 'monthly', 'never'
}
