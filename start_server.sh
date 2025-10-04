#!/bin/bash

# FastAPI MCP Server Startup Script

echo "Starting FastAPI MCP Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server
echo "Starting FastAPI MCP Server on http://localhost:8000"
echo "MCP WebSocket endpoint: ws://localhost:8000/mcp"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"

python main.py
