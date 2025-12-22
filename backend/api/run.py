# Run script for the FastAPI server

import uvicorn


def main():
    """Run the FastAPI server"""
    uvicorn.run(
        "api.app:app",
        host="localhost",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
