import uuid
from typing import Optional, Dict
from sqlalchemy.orm import Session
from backend.database.migrations.chat import ChatSession


class SessionService:
    def __init__(self):
        self._active_sessions: Dict[uuid.UUID, uuid.UUID] = {}

    def get_or_create_session(self, db: Session, user_id: uuid.UUID, 
                            provided_session_id: Optional[uuid.UUID] = None) -> uuid.UUID:
        if provided_session_id:
            if self._verify_session_ownership(db, user_id, provided_session_id):
                self._active_sessions[user_id] = provided_session_id
                return provided_session_id
            else:
                return self._create_new_session(db, user_id)
        
        if user_id in self._active_sessions:
            session_id = self._active_sessions[user_id]
            if self._verify_session_exists(db, session_id):
                return session_id
        
        return self._create_new_session(db, user_id)
    
    def _create_new_session(self, db: Session, user_id: uuid.UUID) -> uuid.UUID:
        session_id = uuid.uuid4()
        
        chat_session = ChatSession(
            id=uuid.uuid4(),
            user_id=user_id,
            session_id=session_id,
            title=None,
            is_active=True
        )
        
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        
        self._active_sessions[user_id] = session_id
        
        return session_id
    
    def _verify_session_exists(self, db: Session, session_id: uuid.UUID) -> bool:
        session = db.query(ChatSession).filter(
            ChatSession.session_id == session_id,
            ChatSession.is_active == True
        ).first()
        
        return session is not None
    
    def _verify_session_ownership(self, db: Session, user_id: uuid.UUID, 
                                session_id: uuid.UUID) -> bool:
        session = db.query(ChatSession).filter(
            ChatSession.session_id == session_id,
            ChatSession.user_id == user_id,
            ChatSession.is_active == True
        ).first()
        
        return session is not None
    
    def get_user_sessions(self, db: Session, user_id: uuid.UUID) -> list:
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.is_active == True
        ).order_by(ChatSession.created_at.desc()).all()
        
        return sessions
    
    def clear_user_active_session(self, user_id: uuid.UUID):
        if user_id in self._active_sessions:
            del self._active_sessions[user_id]
