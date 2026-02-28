@echo off
CLS
echo ====================================
echo  RAG Chatbot - Starting Server
echo ====================================
echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo Error installing dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully.
echo.
echo Starting Flask server...
echo Access the application at: http://localhost:5000
echo.
echo Press CTRL+C to stop the server.
echo.
python app_flask.py
