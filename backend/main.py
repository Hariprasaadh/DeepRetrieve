# DeepRetrieve Backend Entry Point

import argparse
import uvicorn
import os


def run_api(host: str = "localhost", port: int = 8000, reload: bool = True):
    """Run the FastAPI server locally"""
    print(f"🔧 Local Mode - DeepRetrieve API at http://{host}:{port}")
    
    uvicorn.run(
        "api.app:app",
        host=host,
        port=port,
        reload=reload
    )


def run_mcp():
    """Run the MCP server"""
    from mcp_server.server import run_server
    print("🔌 Starting DeepRetrieve MCP Server")
    run_server()


def main():
    parser = argparse.ArgumentParser(description="DeepRetrieve Backend")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["api", "mcp"], 
        default="api",
        help="Run mode: 'api' for FastAPI server, 'mcp' for MCP server"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    args = parser.parse_args()
    
    if args.mode == "api":
        run_api(host=args.host, port=args.port, reload=not args.no_reload)
    else:
        run_mcp()


if __name__ == "__main__":
    main()
