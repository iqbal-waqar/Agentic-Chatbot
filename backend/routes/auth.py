from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.interactors.auth import AuthInteractor
from backend.schemas.auth import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthInteractor.register_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return AuthInteractor.login_user(db, user_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    db: Session = Depends(get_db), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return AuthInteractor.get_current_user(db, credentials.credentials)