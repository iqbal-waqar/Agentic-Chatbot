"""
Services package for the Agentic Chatbot

This package contains all third-party integrations and service classes:
- GeminiService: Google Gemini LLM integration
- GroqService: Groq LLM integration  
- TavilyService: Tavily web search integration
- AgentService: Main agent orchestration with role-based prompts
- AgentRoles: Role definitions and management
- SessionService: Automatic session management for chat conversations
"""

from .gemini import GeminiService
from .groq import GroqService
from .tavily import TavilyService
from .agent import AgentService
from .roles import AgentRoles
from .session import SessionService

__all__ = ['GeminiService', 'GroqService', 'TavilyService', 'AgentService', 'AgentRoles', 'SessionService']