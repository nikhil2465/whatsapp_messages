@echo off
echo ========================================
echo 🚀 Real WhatsApp Business System
echo ========================================
echo.

echo 📋 Checking dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python found

echo 📦 Installing dependencies...
pip install -r requirements_simple.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed

echo 📁 Creating necessary directories...
if not exist logs mkdir logs
if not exist exports mkdir exports

echo ✅ Directories created

echo 🔧 Checking configuration...
if not exist .env (
    echo 📝 Creating .env from real configuration...
    copy .env.real .env
    echo ⚠️ Configuration ready!
    echo 💡 Configure WhatsApp Business API for real messaging, or leave empty for WhatsApp Web fallback
)

echo ✅ Configuration ready

echo.
echo 🚀 Starting Real WhatsApp Business System...
echo 📱 Dashboard: http://localhost:5000
echo 🔗 Webhook: http://localhost:5000/webhook/whatsapp
echo 📊 Google Sheets Export: http://localhost:5000/api/export-google-sheets
echo.
echo 💡 This system supports both real WhatsApp API and WhatsApp Web fallback!
echo 💡 Configure API credentials in the dashboard for real messaging.
echo 💡 Leave empty to use WhatsApp Web links (no registration required).
echo.
echo Press Ctrl+C to stop the server
echo.

python real_main_system.py

pause
