from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.interactors.chat import ChatInteractor
from backend.schemas.chat import ChatRequest, ChatResponse, AvailableModelsResponse
from typing import List
import uuid

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
security = HTTPBearer()

@router.get("/models", response_model=AvailableModelsResponse)
async def get_available_models():
    chat_interactor = ChatInteractor()
    return chat_interactor.get_available_models()

@router.post("/", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    chat_interactor = ChatInteractor()
    return await chat_interactor.process_chat(db, credentials.credentials, chat_request)

@router.get("/history/{session_id}", response_model=List[ChatResponse])
async def get_chat_history(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    chat_interactor = ChatInteractor()
    return chat_interactor.get_chat_history(db, credentials.credentials, session_id)

@router.get("/sessions")
async def get_user_sessions(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    chat_interactor = ChatInteractor()
    return chat_interactor.get_user_sessions(db, credentials.credentials)

@router.post("/new-session")
async def create_new_session(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    chat_interactor = ChatInteractor()
    return chat_interactor.create_new_session(db, credentials.credentials)