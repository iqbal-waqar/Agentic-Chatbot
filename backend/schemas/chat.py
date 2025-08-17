from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid

class ModelProvider(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"

class GeminiModel(str, Enum):
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"

class GroqModel(str, Enum):
    LLAMA_3_3_70B = "llama-3.3-70b-versatile"

class AgentRole(str, Enum):
    CRYPTO_TREND_TELLER = "crypto_trend_teller"
    FINANCIAL_ADVISOR = "financial_advisor"
    TECH_EXPERT = "tech_expert"
    NEWS_ANALYST = "news_analyst"
    TRAVEL_GUIDE = "travel_guide"
    HEALTH_WELLNESS_COACH = "health_wellness_coach"
    BUSINESS_CONSULTANT = "business_consultant"
    DEFAULT = "default"

class ChatRequest(BaseModel):
    session_id: Optional[uuid.UUID] = Field(None, description="Chat session ID (auto-generated if not provided)")
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    model_name: str = Field(..., description="AI model to use")
    model_provider: ModelProvider = Field(..., description="AI provider (gemini or groq)")
    role: Optional[AgentRole] = Field(AgentRole.DEFAULT, description="Agent role to use")
    search_enabled: Optional[bool] = Field(True, description="Enable web search")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Model temperature")

class ChatResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    user_message: str
    ai_response: str
    model_name: str
    model_provider: str
    role: str
    search_enabled: bool
    response_time_ms: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ModelInfo(BaseModel):
    provider: str
    models: List[str]
    current_model: str
    temperature: float

class AvailableModelsResponse(BaseModel):
    gemini: ModelInfo
    groq: ModelInfo
    roles: List[dict]