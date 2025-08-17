import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

class TavilyService:
    def __init__(self):
        self.api_key = os.environ.get("TAVILY_API_KEY")
        
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
    
    def get_search_tool(self, max_results=2):
        return TavilySearchResults(
            max_results=max_results,
            tavily_api_key=self.api_key
        )
    
    def get_service_info(self):
        return {
            "api_key_configured": bool(self.api_key),
            "service_name": "Tavily Search",
            "description": "Web search and information retrieval service"
        }
    
    def is_configured(self):
        return bool(self.api_key)