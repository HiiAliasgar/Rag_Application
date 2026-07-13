@echo off
REM Windows startup script for RAG Application

echo 🚀 Starting RAG Application...

REM Check for .env file
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    copy .env.example .env
    echo Please edit .env and add your OPENAI_API_KEY
    exit /b 1
)

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

echo ✅ Python installed

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -q -r requirements.txt

REM Create data directories
if not exist data\uploads mkdir data\uploads
if not exist data\chroma_db mkdir data\chroma_db

echo.
echo ✅ Setup complete!
echo.
echo 🔧 Starting services...
echo.
echo 💻 API Server: http://localhost:8000
echo 🎨 UI Server: http://localhost:8501
echo.
echo Starting API Server in new window...
start "RAG API" cmd /k "python -m src.app"

timeout /t 2 /nobreak

echo Starting Streamlit in new window...
start "RAG UI" cmd /k "streamlit run src/streamlit_ui.py --server.port=8501 --server.address=0.0.0.0"

echo.
echo ✅ Both services started!
echo Close windows to stop services.
echo.

pause
