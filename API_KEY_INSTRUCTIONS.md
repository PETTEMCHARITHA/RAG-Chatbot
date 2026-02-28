# API Key Configuration

## To Change the Gemini API Key:

1. Open the `config.py` file
2. Find this line:
   ```python
   GEMINI_API_KEY = "AIzaSyBM7Fd6nh5xLzdzbIO8kEoohYKvc6zhQEQ"
   ```
3. Replace the key with your own API key
4. Save the file
5. Restart the Flask server

## Where to Get Your API Key:

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in the `config.py` file

## Important Notes:

- The API key shown is for demonstration purposes
- If you're getting errors, try generating a new API key
- Make sure your API key has access to the Gemini API
- Keep your API key private and never share it publicly

## Other Configuration Options:

All configuration options are in `config.py`:
- `FLASK_SECRET_KEY` - Change this for production
- `DEBUG` - Set to False for production
- `PORT` - Server port (default: 5000)
- `HOST` - Server host (default: 127.0.0.1)
- `MAX_CONTENT_LENGTH` - Maximum file upload size
