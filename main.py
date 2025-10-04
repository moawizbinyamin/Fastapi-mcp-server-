from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio
from typing import Dict, Any, List
import logging
import os
import hashlib
import uuid
import random
import datetime
import re
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI MCP Server",
    description="A FastAPI application with MCP (Model Context Protocol) server functionality",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP Protocol Models
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    result: Dict[str, Any] = {}
    error: Dict[str, Any] = None

class MCPNotification(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = {}

# MCP Server Implementation
class MCPServer:
    def __init__(self):
        self.tools = {
            # Basic tools
            "echo": {
                "name": "echo",
                "description": "Echo back the input text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to echo back"
                        }
                    },
                    "required": ["text"]
                }
            },
            "get_time": {
                "name": "get_time",
                "description": "Get current server time",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            
            # Mathematical operations
            "add": {
                "name": "add",
                "description": "Add two numbers together",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number"
                        }
                    },
                    "required": ["a", "b"]
                }
            },
            "subtract": {
                "name": "subtract",
                "description": "Subtract second number from first number",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number"
                        }
                    },
                    "required": ["a", "b"]
                }
            },
            "multiply": {
                "name": "multiply",
                "description": "Multiply two numbers",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number"
                        }
                    },
                    "required": ["a", "b"]
                }
            },
            "divide": {
                "name": "divide",
                "description": "Divide first number by second number",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number"
                        }
                    },
                    "required": ["a", "b"]
                }
            },
            "power": {
                "name": "power",
                "description": "Raise first number to the power of second number",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "base": {
                            "type": "number",
                            "description": "Base number"
                        },
                        "exponent": {
                            "type": "number",
                            "description": "Exponent"
                        }
                    },
                    "required": ["base", "exponent"]
                }
            },
            "sqrt": {
                "name": "sqrt",
                "description": "Calculate square root of a number",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "number": {
                            "type": "number",
                            "description": "Number to calculate square root of"
                        }
                    },
                    "required": ["number"]
                }
            },
            
            # String operations
            "uppercase": {
                "name": "uppercase",
                "description": "Convert text to uppercase",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to convert to uppercase"
                        }
                    },
                    "required": ["text"]
                }
            },
            "lowercase": {
                "name": "lowercase",
                "description": "Convert text to lowercase",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to convert to lowercase"
                        }
                    },
                    "required": ["text"]
                }
            },
            "reverse_string": {
                "name": "reverse_string",
                "description": "Reverse a string",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to reverse"
                        }
                    },
                    "required": ["text"]
                }
            },
            "string_length": {
                "name": "string_length",
                "description": "Get the length of a string",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to measure"
                        }
                    },
                    "required": ["text"]
                }
            },
            
            # File operations
            "read_file": {
                "name": "read_file",
                "description": "Read contents of a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path to the file to read"
                        }
                    },
                    "required": ["filepath"]
                }
            },
            "write_file": {
                "name": "write_file",
                "description": "Write content to a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path to the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["filepath", "content"]
                }
            },
            "list_directory": {
                "name": "list_directory",
                "description": "List files and directories in a path",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path to list"
                        }
                    },
                    "required": ["path"]
                }
            },
            
            # Utility functions
            "random_number": {
                "name": "random_number",
                "description": "Generate a random number between min and max",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "min": {
                            "type": "number",
                            "description": "Minimum value"
                        },
                        "max": {
                            "type": "number",
                            "description": "Maximum value"
                        }
                    },
                    "required": ["min", "max"]
                }
            },
            "generate_uuid": {
                "name": "generate_uuid",
                "description": "Generate a random UUID",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            "hash_md5": {
                "name": "hash_md5",
                "description": "Generate MD5 hash of input text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to hash"
                        }
                    },
                    "required": ["text"]
                }
            },
            "hash_sha256": {
                "name": "hash_sha256",
                "description": "Generate SHA256 hash of input text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to hash"
                        }
                    },
                    "required": ["text"]
                }
            },
            
            # Web utilities
            "validate_url": {
                "name": "validate_url",
                "description": "Validate if a string is a valid URL",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to validate"
                        }
                    },
                    "required": ["url"]
                }
            },
            "make_request": {
                "name": "make_request",
                "description": "Make an HTTP request to a URL",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to request"
                        },
                        "method": {
                            "type": "string",
                            "description": "HTTP method (GET, POST, etc.)",
                            "default": "GET"
                        },
                        "headers": {
                            "type": "object",
                            "description": "HTTP headers",
                            "default": {}
                        }
                    },
                    "required": ["url"]
                }
            }
        }
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle MCP requests"""
        try:
            if request.method == "initialize":
                return MCPResponse(
                    id=request.id,
                    result={
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "fastapi-mcp-server",
                            "version": "1.0.0"
                        }
                    }
                )
            
            elif request.method == "tools/list":
                return MCPResponse(
                    id=request.id,
                    result={
                        "tools": list(self.tools.values())
                    }
                )
            
            elif request.method == "tools/call":
                tool_name = request.params.get("name")
                arguments = request.params.get("arguments", {})
                
                if tool_name in self.tools:
                    result = await self.call_tool(tool_name, arguments)
                    return MCPResponse(
                        id=request.id,
                        result={
                            "content": [
                                {
                                    "type": "text",
                                    "text": str(result)
                                }
                            ]
                        }
                    )
                else:
                    return MCPResponse(
                        id=request.id,
                        error={
                            "code": -32601,
                            "message": f"Tool '{tool_name}' not found"
                        }
                    )
            
            else:
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32601,
                        "message": f"Method '{request.method}' not found"
                    }
                )
        
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            )
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a specific tool with given arguments"""
        
        # Basic tools
        if tool_name == "echo":
            return arguments.get("text", "")
        
        elif tool_name == "get_time":
            return datetime.datetime.now().isoformat()
        
        # Mathematical operations
        elif tool_name == "add":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            return a + b
        
        elif tool_name == "subtract":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            return a - b
        
        elif tool_name == "multiply":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            return a * b
        
        elif tool_name == "divide":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            if b == 0:
                raise ValueError("Division by zero is not allowed")
            return a / b
        
        elif tool_name == "power":
            base = arguments.get("base", 0)
            exponent = arguments.get("exponent", 0)
            return base ** exponent
        
        elif tool_name == "sqrt":
            number = arguments.get("number", 0)
            if number < 0:
                raise ValueError("Cannot calculate square root of negative number")
            return number ** 0.5
        
        # String operations
        elif tool_name == "uppercase":
            text = arguments.get("text", "")
            return text.upper()
        
        elif tool_name == "lowercase":
            text = arguments.get("text", "")
            return text.lower()
        
        elif tool_name == "reverse_string":
            text = arguments.get("text", "")
            return text[::-1]
        
        elif tool_name == "string_length":
            text = arguments.get("text", "")
            return len(text)
        
        # File operations
        elif tool_name == "read_file":
            filepath = arguments.get("filepath", "")
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                raise ValueError(f"File not found: {filepath}")
            except Exception as e:
                raise ValueError(f"Error reading file: {str(e)}")
        
        elif tool_name == "write_file":
            filepath = arguments.get("filepath", "")
            content = arguments.get("content", "")
            try:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                return f"Successfully wrote {len(content)} characters to {filepath}"
            except Exception as e:
                raise ValueError(f"Error writing file: {str(e)}")
        
        elif tool_name == "list_directory":
            path = arguments.get("path", ".")
            try:
                items = os.listdir(path)
                return {
                    "path": path,
                    "items": items,
                    "count": len(items)
                }
            except FileNotFoundError:
                raise ValueError(f"Directory not found: {path}")
            except Exception as e:
                raise ValueError(f"Error listing directory: {str(e)}")
        
        # Utility functions
        elif tool_name == "random_number":
            min_val = arguments.get("min", 0)
            max_val = arguments.get("max", 100)
            if min_val > max_val:
                raise ValueError("Minimum value cannot be greater than maximum value")
            return random.randint(int(min_val), int(max_val))
        
        elif tool_name == "generate_uuid":
            return str(uuid.uuid4())
        
        elif tool_name == "hash_md5":
            text = arguments.get("text", "")
            return hashlib.md5(text.encode()).hexdigest()
        
        elif tool_name == "hash_sha256":
            text = arguments.get("text", "")
            return hashlib.sha256(text.encode()).hexdigest()
        
        # Web utilities
        elif tool_name == "validate_url":
            url = arguments.get("url", "")
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return bool(url_pattern.match(url))
        
        elif tool_name == "make_request":
            url = arguments.get("url", "")
            method = arguments.get("method", "GET").upper()
            headers = arguments.get("headers", {})
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.request(method, url, headers=headers)
                    return {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "content": response.text,
                        "url": str(response.url)
                    }
            except Exception as e:
                raise ValueError(f"Error making request: {str(e)}")
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

# Initialize MCP Server
mcp_server = MCPServer()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New MCP connection established. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"MCP connection closed. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

# FastAPI Routes
@app.get("/")
async def root():
    return {
        "message": "FastAPI MCP Server is running!",
        "version": "1.0.0",
        "mcp_endpoint": "/mcp",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "active_connections": len(manager.active_connections)}

@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {"tools": list(mcp_server.tools.values())}

@app.post("/tools/call")
async def call_tool(request: dict):
    """Call a tool via HTTP endpoint"""
    tool_name = request.get("name")
    arguments = request.get("arguments", {})
    
    if tool_name in mcp_server.tools:
        result = await mcp_server.call_tool(tool_name, arguments)
        return {"result": result}
    else:
        return {"error": f"Tool '{tool_name}' not found"}

@app.websocket("/mcp")
async def websocket_endpoint(websocket: WebSocket):
    """MCP WebSocket endpoint"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            logger.info(f"Received MCP message: {data}")
            
            try:
                # Parse JSON-RPC request
                request_data = json.loads(data)
                request = MCPRequest(**request_data)
                
                # Handle the request
                response = await mcp_server.handle_request(request)
                
                # Send response
                await manager.send_personal_message(response.model_dump_json(), websocket)
                logger.info(f"Sent MCP response: {response.model_dump_json()}")
                
            except json.JSONDecodeError:
                error_response = MCPResponse(
                    id="unknown",
                    error={
                        "code": -32700,
                        "message": "Parse error"
                    }
                )
                await manager.send_personal_message(error_response.model_dump_json(), websocket)
            
            except Exception as e:
                logger.error(f"Error processing MCP message: {e}")
                error_response = MCPResponse(
                    id="unknown",
                    error={
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                )
                await manager.send_personal_message(error_response.model_dump_json(), websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
