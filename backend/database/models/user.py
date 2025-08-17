from sqlalchemy.orm import Session
from ..migrations.user import User
import uuid
from typing import Optional

class UserModel:
    @staticmethod
    def create_user(db: Session, username: str, email: str, password_hash: str) -> User:
        user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=password_hash
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()