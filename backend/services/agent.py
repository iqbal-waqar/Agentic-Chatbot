from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import SystemMessage
from .gemini import GeminiService
from .groq import GroqService
from .tavily import TavilyService
from .roles import AgentRoles

load_dotenv()

class AgentService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.groq_service = GroqService()
        self.tavily_service = TavilyService()
        self.agent_roles = AgentRoles()
    
    def get_search_tool(self, max_results=2):
        return self.tavily_service.get_search_tool(max_results)
    
    def get_llm_by_provider(self, provider, model=None, temperature=None):
        if provider.lower() == "gemini":
            return self.gemini_service.get_llm(model, temperature)
        elif provider.lower() == "groq":
            return self.groq_service.get_llm(model, temperature)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'Gemini' or 'Groq'")
    
    def create_role_based_system_prompt(self, role):
        return self.agent_roles.get_role_prompt(role)
    
    def get_response_from_ai_agent(self, provider, query, role="default", allow_search=True, model=None, temperature=None):
        try:
            llm = self.get_llm_by_provider(provider, model, temperature)
            
            tools = [self.get_search_tool()] if allow_search else []
            
            system_prompt = self.create_role_based_system_prompt(role)
            
            agent = create_react_agent(
                model=llm,
                tools=tools,
                prompt=SystemMessage(content=system_prompt)
            )
            
            if isinstance(query, str):
                state = {"messages": [{"role": "user", "content": query}]}
            else:
                state = {"messages": query}
            
            response = agent.invoke(state)
            messages = response.get("messages", [])
            
            ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
            
            return ai_messages[-1] if ai_messages else "I apologize, but I couldn't generate a response."
            
        except Exception as e:
            return f"Error: {str(e)}"
    