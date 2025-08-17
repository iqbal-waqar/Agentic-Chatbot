import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        self.temperature = float(os.environ.get("GEMINI_TEMPERATURE", "0.7"))
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    def get_llm(self, model=None, temperature=None):
        model_name = model or self.model
        temp = temperature if temperature is not None else self.temperature
        
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=self.api_key,
            temperature=temp
        )
    
    def get_available_models(self):
        return [
            "gemini-2.0-flash",
            "gemini-1.5-flash",
        ]
    
    def get_model_info(self):
        return {
            "current_model": self.model,
            "temperature": self.temperature,
            "api_key_configured": bool(self.api_key),
            "available_models": self.get_available_models()
        }
    