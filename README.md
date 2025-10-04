# FastAPI MCP Server

A comprehensive FastAPI application with Model Context Protocol (MCP) server functionality, providing 21+ useful tools for mathematical operations, string manipulation, file handling, utilities, and web requests.

## 🎥 Demo Video

### 📺 Watch the Demo

**Google Drive:** [FastAPI MCP Server Demo Video](https://drive.google.com/file/d/YOUR_VIDEO_ID/view?usp=sharing)

*Click the link above to watch the demonstration video showing all 21+ tools in action!*

### 📋 How to Use Google Drive Links:

1. **Upload your video** to Google Drive
2. **Right-click** on the video file → "Get link"
3. **Change permissions** to "Anyone with the link can view"
4. **Copy the sharing link** and replace `YOUR_VIDEO_ID` above

### 🔗 Alternative Hosting Options:
- **[YouTube](https://youtube.com)** - Best for public demos with embed preview
- **[GitHub Releases](https://github.com/moawizbinyamin/Fastapi-mcp-server-/releases)** - For downloadable files
- **[GitHub Pages](https://pages.github.com)** - For project websites
- **[Vimeo](https://vimeo.com)** - Professional video hosting

## Features

### 🔢 Mathematical Operations
- **add** - Add two numbers together
- **subtract** - Subtract second number from first number
- **multiply** - Multiply two numbers
- **divide** - Divide first number by second number (with zero-division protection)
- **power** - Raise first number to the power of second number
- **sqrt** - Calculate square root of a number

### 📝 String Operations
- **echo** - Echo back the input text
- **uppercase** - Convert text to uppercase
- **lowercase** - Convert text to lowercase
- **reverse_string** - Reverse a string
- **string_length** - Get the length of a string

### 📁 File Operations
- **read_file** - Read contents of a file
- **write_file** - Write content to a file
- **list_directory** - List files and directories in a path

### 🛠️ Utility Functions
- **get_time** - Get current server time
- **random_number** - Generate a random number between min and max
- **generate_uuid** - Generate a random UUID
- **hash_md5** - Generate MD5 hash of input text
- **hash_sha256** - Generate SHA256 hash of input text

### 🌐 Web Utilities
- **validate_url** - Validate if a string is a valid URL
- **make_request** - Make an HTTP request to a URL

## Installation

1. Clone the repository:
```bash
git clone https://github.com/moawizbinyamin/Fastapi-mcp-server-.git
cd Fastapi-mcp-server-
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### Available Endpoints

- **GET /** - Root endpoint with server info
- **GET /health** - Health check endpoint
- **GET /tools** - List all available tools
- **POST /tools/call** - Call tools via HTTP
- **WebSocket /mcp** - MCP protocol endpoint
- **GET /docs** - FastAPI automatic documentation

### Testing Tools via HTTP

#### List all tools:
```bash
curl http://localhost:8000/tools
```

#### Call a tool:
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "add", "arguments": {"a": 5, "b": 3}}'
```

#### Example: Mathematical operations on 2 and 4:
```bash
# Addition: 2 + 4 = 6
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "add", "arguments": {"a": 2, "b": 4}}'

# Subtraction: 2 - 4 = -2
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "subtract", "arguments": {"a": 2, "b": 4}}'

# Multiplication: 2 × 4 = 8
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "multiply", "arguments": {"a": 2, "b": 4}}'

# Division: 2 ÷ 4 = 0.5
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "divide", "arguments": {"a": 2, "b": 4}}'

# Power: 2^4 = 16
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "power", "arguments": {"base": 2, "exponent": 4}}'
```

## MCP Protocol Support

This server implements the Model Context Protocol (MCP) specification, allowing it to be used with MCP-compatible clients. The WebSocket endpoint `/mcp` handles MCP protocol communication.

### MCP Configuration

For use with MCP clients, configure your MCP client with:

```json
{
  "mcpServers": {
    "fastapi-mcp-server": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/Fastapi-mcp-server-",
      "env": {
        "PYTHONPATH": "/path/to/Fastapi-mcp-server-"
      }
    }
  }
}
```

## Dependencies

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server implementation
- **Pydantic** - Data validation using Python type annotations
- **httpx** - HTTP client for making web requests
- **websockets** - WebSocket implementation

## Error Handling

All tools include comprehensive error handling:
- Division by zero protection
- File not found handling
- Invalid input validation
- Network request error handling

## Development

### Project Structure
```
Fastapi-mcp-server-/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
├── start_server.bat    # Windows startup script
└── start_server.sh     # Linux/Mac startup script
```

### Adding New Tools

To add a new tool:

1. Add the tool definition to the `tools` dictionary in the `MCPServer.__init__()` method
2. Add the tool implementation to the `call_tool()` method
3. Test the tool via the HTTP endpoint

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue on the GitHub repository.