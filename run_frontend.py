#!/usr/bin/env python3
"""
Frontend Server Launcher
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit frontend"""
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, "frontend")
    app_path = os.path.join(frontend_dir, "app.py")
    
    print("🚀 Starting Agentic Chatbot Frontend...")
    print("📱 Frontend will be available at: http://localhost:8501")
    print("🔗 Make sure backend is running at: http://127.0.0.1:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        requirements_path = os.path.join(frontend_dir, "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Launch streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--theme.primaryColor", "#1f77b4",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f0f2f6"
        ])
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped!")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        print("💡 Make sure you have installed frontend dependencies:")
        print("   cd frontend && pip install -r requirements.txt")

if __name__ == "__main__":
    main()