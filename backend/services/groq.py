import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.temperature = float(os.environ.get("GROQ_TEMPERATURE", "0.7"))
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
    
    def get_llm(self, model=None, temperature=None):
        model_name = model or self.model
        temp = temperature if temperature is not None else self.temperature
        
        return ChatGroq(
            model=model_name,
            groq_api_key=self.api_key,
            temperature=temp
        )
    
    def get_available_models(self):
        return [
            "llama-3.3-70b-versatile",
        ]
    
    def get_model_info(self):
        return {
            "current_model": self.model,
            "temperature": self.temperature,
            "api_key_configured": bool(self.api_key),
            "available_models": self.get_available_models()
        }
    