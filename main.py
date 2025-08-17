"""
Main FastAPI application for Agentic Chatbot
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth, chat

app = FastAPI(
    title="Agentic Chatbot API",
    description="An intelligent AI chatbot with multiple roles, web search capabilities, and support for multiple LLM providers (Gemini & Groq)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/", tags=["🏠 Home"])
def read_home():
    """
    Welcome endpoint with API information
    """
    return {
        "message": "Welcome to the Agentic Chatbot API! 🤖",
        "version": "1.0.0",
        "description": "An intelligent AI chatbot with role-based responses and web search capabilities",
        "features": [
            "🤖 Multiple AI agent roles (Tech Expert, Crypto Trend Teller, Default Assistant, etc.)",
            "🔍 Web search integration with Tavily",
            "🧠 Multiple LLM providers (Google Gemini & Groq)",
            "⚙️ Configurable models and temperature settings",
            "📝 Role-based system prompts for specialized responses"
        ],
        "supported_providers": [
            "Google Gemini (gemini-2.0-flash, gemini-1.5-pro, etc.)",
            "Groq (llama-3.3-70b-versatile, mixtral-8x7b-32768, etc.)"
        ],
    }

@app.get("/health", tags=["🏥 Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "Agentic Chatbot API is running successfully! 🚀"
    }