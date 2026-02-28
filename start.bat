@echo off
echo ====================================
echo  RAG Chatbot - Starting Server
echo ====================================
echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo.
echo Access the application at: http://localhost:5000
echo.
python app_flask.py
pause
