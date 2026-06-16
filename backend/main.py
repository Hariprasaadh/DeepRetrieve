# Purpose: Entrypoint script for starting the backend API and MCP services.
# Responsibilities: Configures execution pathways to launch either the FastAPI application 
# server (with auto-reload) or the FastMCP server wrapper.

import uvicorn



def run_api():
    """Starts the FastAPI application server with auto-reload for local development."""
    print("🔧 Local Mode - DeepRetrieve API at http://localhost:8000")
    
    uvicorn.run(
        "api.app:app",
        host="localhost",
        port=8000,
        reload=True
    )


def run_mcp():
    """Starts the FastMCP server, exposing RAG tools to compliant MCP clients."""
    from mcp_server.server import run_server
    print("🔌 Starting DeepRetrieve MCP Server")
    run_server()


def main():
    run_api()


if __name__ == "__main__":
    main()

