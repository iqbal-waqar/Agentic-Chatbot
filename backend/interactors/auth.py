from sqlalchemy.orm import Session
from backend.database.models.user import UserModel
from backend.schemas.auth import UserCreate, UserLogin, Token
from backend.services.auth import AuthService
from fastapi import HTTPException, status
import uuid

class AuthInteractor:
    def register_user(db: Session, user_data: UserCreate):
        existing_user = UserModel.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        password_hash = AuthService.hash_password(user_data.password)
        user = UserModel.create_user(db, user_data.username, user_data.email, password_hash)
        return user
    
    def login_user(db: Session, user_data: UserLogin):
        user = UserModel.get_user_by_username(db, user_data.username)
        if not user or not AuthService.verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        access_token = AuthService.create_access_token({"sub": str(user.id)})
        return Token(access_token=access_token)
    
    def get_current_user(db: Session, token: str):
        try:
            payload = AuthService.verify_token(token)
            user_id = uuid.UUID(payload.get("sub"))
            user = UserModel.get_user_by_id(db, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            return user
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
