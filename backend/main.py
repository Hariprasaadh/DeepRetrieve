# DeepRetrieve Backend Entry Point

import uvicorn


def run_api():
    """Run the FastAPI server locally"""
    print("🔧 Local Mode - DeepRetrieve API at http://localhost:8000")
    
    uvicorn.run(
        "api.app:app",
        host="localhost",
        port=8000,
        reload=True
    )


def run_mcp():
    """Run the MCP server"""
    from mcp_server.server import run_server
    print("🔌 Starting DeepRetrieve MCP Server")
    run_server()


def main():
    run_api()


if __name__ == "__main__":
    main()
