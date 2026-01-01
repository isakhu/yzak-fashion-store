@echo off
echo.
echo ========================================
echo    🏪 YZAK FASHION STORE STARTING...
echo ========================================
echo.
echo 🇪🇹 Dire Dawa • Hawassa Branches
echo.

cd /d "%~dp0"

echo 📦 Installing packages...
pip install fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv alembic email-validator requests

echo.
echo 🗄️ Setting up database...
python init_db.py

echo.
echo 🚀 Starting Yzak Fashion Store...
echo.
echo ✅ Your store will open at: http://localhost:8000
echo ✅ Login: admin / admin
echo.
echo Press Ctrl+C to stop the server
echo.

python -m app.main

pause