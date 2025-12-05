# DeepRetrieve Backend Entry Point

import argparse
import uvicorn
import os


def run_api(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """Run the FastAPI server"""
    # Auto-detect environment
    is_render = os.getenv("RENDER") is not None
    is_production = os.getenv("PYTHON_ENV") == "production" or is_render
    
    # For Render deployment
    port = int(os.getenv("PORT", port))
    
    # Auto-configure host based on environment
    if is_production:
        host = "0.0.0.0"
        reload = False
        print(f"🌐 Production Mode - DeepRetrieve API at http://{host}:{port}")
    else:
        host = "localhost"
        print(f"🔧 Development Mode - DeepRetrieve API at http://{host}:{port}")
    
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
