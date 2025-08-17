from sqlalchemy.orm import Session
from ..migrations.chat import Chat, ChatSession
import uuid
from typing import List, Optional

class ChatSessionModel:
    @staticmethod
    def create_session(db: Session, user_id: uuid.UUID, session_id: uuid.UUID, 
                      title: str = None) -> ChatSession:
        chat_session = ChatSession(
            id=uuid.uuid4(),
            user_id=user_id,
            session_id=session_id,
            title=title,
            is_active=True
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        return chat_session
    
    @staticmethod
    def get_session_by_id(db: Session, session_id: uuid.UUID) -> Optional[ChatSession]:
        return db.query(ChatSession).filter(
            ChatSession.session_id == session_id,
            ChatSession.is_active == True
        ).first()
    
    @staticmethod
    def get_user_sessions(db: Session, user_id: uuid.UUID) -> List[ChatSession]:
        return db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.is_active == True
        ).order_by(ChatSession.created_at.desc()).all()

class ChatModel:
    @staticmethod
    def create_chat(db: Session, user_id: uuid.UUID, session_id: uuid.UUID, 
                   model_name: str, model_provider: str, user_message: str, 
                   ai_response: str, role: str = "default", search_enabled: bool = True,
                   system_prompt: str = None, response_time_ms: int = None) -> Chat:
        chat = Chat(
            id=uuid.uuid4(),
            user_id=user_id,
            session_id=session_id,
            model_name=model_name,
            model_provider=model_provider,
            role=role,
            system_prompt=system_prompt,
            user_message=user_message,
            ai_response=ai_response,
            search_enabled=search_enabled,
            response_time_ms=response_time_ms
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat
    
    @staticmethod
    def get_chat_history(db: Session, session_id: uuid.UUID) -> List[Chat]:
        return db.query(Chat).filter(
            Chat.session_id == session_id
        ).order_by(Chat.created_at.asc()).all()