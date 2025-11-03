#!/bin/bash

# CompetiScope Agent Deployment Script

echo "🚀 Deploying CompetiScope Agent..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.13+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -e .

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running the agent."
fi

# Check environment variables
echo "🔍 Checking configuration..."
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
if not gemini_key or gemini_key == 'your_gemini_api_key_here':
    print('❌ Please set your GEMINI_API_KEY in the .env file')
    exit(1)
else:
    print('✅ GEMINI_API_KEY is configured')

print('✅ Configuration looks good!')
"

if [ $? -eq 0 ]; then
    echo "🎉 Deployment successful!"
    echo ""
    echo "To start the agent:"
    echo "  uvicorn main:app --reload --port 8000"
    echo ""
    echo "To test the agent:"
    echo "  python test_agent.py"
    echo ""
    echo "API will be available at: http://localhost:8000"
    echo "API docs will be available at: http://localhost:8000/docs"
else
    echo "❌ Deployment failed. Please check your configuration."
    exit 1
fi