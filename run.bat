@echo off
echo 🚀 Starting E-Commerce API Server
echo ================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup first: python setup.py
    pause
    exit /b 1
)

REM Activate virtual environment and start server
echo ✅ Activating virtual environment...
call venv\Scripts\activate

echo ✅ Starting FastAPI server...
echo 🌐 Server will be available at: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m app.main

pause