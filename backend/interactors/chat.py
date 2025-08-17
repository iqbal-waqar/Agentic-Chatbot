from sqlalchemy.orm import Session
from backend.database.models.chat import ChatModel
from backend.schemas.chat import ChatRequest, AvailableModelsResponse, ModelInfo
from backend.services.agent import AgentService
from backend.services.session import SessionService
from backend.services.gemini import GeminiService
from backend.services.groq import GroqService
from backend.services.roles import AgentRoles
from fastapi import HTTPException, status
from typing import List
import uuid

class ChatInteractor:
    async def process_chat(self, db: Session, token: str, chat_request: ChatRequest):
        try:
            # Import here to avoid circular imports
            from backend.interactors.auth import AuthInteractor
            
            # Get current user from token
            current_user = AuthInteractor.get_current_user(db, token)
            
            # Get or create session automatically
            session_service = SessionService()
            session_id = session_service.get_or_create_session(
                db=db,
                user_id=current_user.id,
                provided_session_id=chat_request.session_id
            )
            
            agent_service = AgentService()
            ai_response = agent_service.get_response_from_ai_agent(
                provider=chat_request.model_provider,
                query=chat_request.message,
                role=chat_request.role or "default",
                allow_search=chat_request.search_enabled,
                model=chat_request.model_name,
                temperature=chat_request.temperature
            )
            
            chat = ChatModel.create_chat(
                db=db,
                user_id=current_user.id,
                session_id=session_id,
                model_name=chat_request.model_name,
                model_provider=chat_request.model_provider,
                user_message=chat_request.message,
                ai_response=ai_response,
                role=chat_request.role or "default",
                search_enabled=chat_request.search_enabled
            )
            
            return chat
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing chat: {str(e)}"
            )

    def get_chat_history(self, db: Session, token: str, session_id: uuid.UUID) -> List:
        try:
            # Import here to avoid circular imports
            from backend.interactors.auth import AuthInteractor
            
            # Get current user from token
            current_user = AuthInteractor.get_current_user(db, token)
            
            chats = ChatModel.get_chat_history(db, session_id)
            
            # Filter chats to only return user's own chats
            user_chats = [chat for chat in chats if chat.user_id == current_user.id]
            
            return user_chats
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting chat history: {str(e)}"
            )

    def get_user_sessions(self, db: Session, token: str):
        """Get formatted user sessions"""
        try:
            # Import here to avoid circular imports
            from backend.interactors.auth import AuthInteractor
            
            # Get current user from token
            current_user = AuthInteractor.get_current_user(db, token)
            
            session_service = SessionService()
            sessions = session_service.get_user_sessions(db, current_user.id)
            return {
                "sessions": [
                    {
                        "session_id": session.session_id,
                        "title": session.title,
                        "created_at": session.created_at,
                        "updated_at": session.updated_at,
                        "is_active": session.is_active
                    }
                    for session in sessions
                ]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting user sessions: {str(e)}"
            )
    
    def create_new_session(self, db: Session, token: str):
        try:
            # Import here to avoid circular imports
            from backend.interactors.auth import AuthInteractor
            
            # Get current user from token
            current_user = AuthInteractor.get_current_user(db, token)
            
            # Clear current active session and create new one
            session_service = SessionService()
            session_service.clear_user_active_session(current_user.id)
            session_id = session_service.get_or_create_session(db, current_user.id)
            return {"session_id": session_id, "message": "New session created"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating new session: {str(e)}"
            )
    
    def get_available_models(self) -> AvailableModelsResponse:
        """Get all available models and roles for dropdown selection"""
        try:
            gemini_service = GeminiService()
            groq_service = GroqService()
            
            gemini_info = gemini_service.get_model_info()
            groq_info = groq_service.get_model_info()
            
            return AvailableModelsResponse(
                gemini=ModelInfo(
                    provider="gemini",
                    models=gemini_info["available_models"],
                    current_model=gemini_info["current_model"],
                    temperature=gemini_info["temperature"]
                ),
                groq=ModelInfo(
                    provider="groq", 
                    models=groq_info["available_models"],
                    current_model=groq_info["current_model"],
                    temperature=groq_info["temperature"]
                ),
                roles=[
                    {"id": role_id, "name": role_data["name"], "description": role_data["description"]}
                    for role_id, role_data in AgentRoles().get_roles_summary().items()
                ]
            )
        except Exception as e:
            # Return default values if services fail
            return AvailableModelsResponse(
                gemini=ModelInfo(
                    provider="gemini",
                    models=["gemini-2.0-flash", "gemini-1.5-pro"],
                    current_model="gemini-2.0-flash",
                    temperature=0.7
                ),
                groq=ModelInfo(
                    provider="groq",
                    models=["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
                    current_model="llama-3.3-70b-versatile", 
                    temperature=0.7
                ),
                roles=[
                    {"id": "default", "name": "AI Assistant", "description": "Smart and friendly AI chatbot"}
                ]
            )