import subprocess
import sys
import os
import time
import signal
import threading

class ServiceManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
    def start_backend(self):
        """Start the backend server"""
        print("🚀 Starting Backend Server...")
        os.chdir(self.project_root)
        
        self.backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
        
    def start_frontend(self):
        """Start the frontend server"""
        print("🚀 Starting Frontend Server...")
        frontend_dir = os.path.join(self.project_root, "frontend")
        os.chdir(frontend_dir)
        
        # Check if streamlit is installed
        try:
            import streamlit
        except ImportError:
            print("❌ Streamlit not found. Installing...")
            requirements_path = os.path.join(frontend_dir, "requirements.txt")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        
        self.frontend_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--theme.primaryColor", "#1f77b4",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f0f2f6"
        ])
        
    def stop_services(self):
        """Stop both services"""
        print("\n🛑 Stopping services...")
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
            print("✅ Backend stopped")
            
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
            print("✅ Frontend stopped")
    
    def run(self):
        """Run both services"""
        print("🤖 Agentic Chatbot - Starting Both Services")
        print("=" * 50)
        
        try:
            # Start backend first
            self.start_backend()
            print("⏳ Waiting for backend to start...")
            time.sleep(3)
            
            # Start frontend
            self.start_frontend()
            print("⏳ Waiting for frontend to start...")
            time.sleep(3)
            
            print("\n✅ Both services are starting!")
            print("🌐 Backend API: http://127.0.0.1:8000")
            print("📚 API Docs: http://127.0.0.1:8000/docs")
            print("📱 Frontend: http://localhost:8501")
            print("\n🛑 Press Ctrl+C to stop both services")
            print("-" * 50)
            
            # Wait for processes
            while True:
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend process died!")
                    break
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend process died!")
                    break
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.stop_services()

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Received interrupt signal...")
    sys.exit(0)

def main():
    """Main function"""
    signal.signal(signal.SIGINT, signal_handler)
    
    manager = ServiceManager()
    manager.run()

if __name__ == "__main__":
    main()