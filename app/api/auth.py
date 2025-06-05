from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, Token, UserResponse
from app.services.auth_service import create_user, authenticate_user, get_user_by_email, get_user_by_username
from app.utils.security import create_access_token
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user_by_username = get_user_by_username(db, user.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    db_user_by_email = get_user_by_email(db, user.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    db_user = create_user(db, user)
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

from app.utils.security import get_current_user

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    """Отримати інформацію про поточного користувача"""
    return current_user