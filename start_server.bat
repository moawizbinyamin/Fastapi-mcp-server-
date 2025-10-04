@echo off
REM FastAPI MCP Server Startup Script for Windows

echo Starting FastAPI MCP Server...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo Starting FastAPI MCP Server on http://localhost:8000
echo MCP WebSocket endpoint: ws://localhost:8000/mcp
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server

python main.py
