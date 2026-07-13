#!/bin/bash

echo "🚀 Starting RAG Application..."

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "Please edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Create data directories
mkdir -p data/uploads data/chroma_db

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔧 Starting services..."
echo ""
echo "💻 API Server: http://localhost:8000"
echo "🎨 UI Server: http://localhost:8501"
echo ""
echo "Starting API (Terminal 1)..."
python -m src.app &
API_PID=$!

sleep 2

echo "Starting Streamlit (Terminal 2)..."
streamlit run src/streamlit_ui.py --server.port=8501 --server.address=0.0.0.0 &
UI_PID=$!

echo ""
echo "✅ Both services started!"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

wait
