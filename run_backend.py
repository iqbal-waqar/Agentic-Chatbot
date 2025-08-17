#!/usr/bin/env python3
"""
Backend Server Launcher
"""

import subprocess
import sys
import os

def main():
    """Launch the FastAPI backend server"""
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Starting Agentic Chatbot Backend...")
    print("🌐 Backend API will be available at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Change to project directory
    os.chdir(project_root)
    
    # Launch FastAPI with uvicorn
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped!")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()