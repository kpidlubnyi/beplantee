from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.password_reset import PasswordResetRequest, PasswordReset
from app.services.password_reset_service import verify_email_exists, reset_password_by_email
from app.database import get_db

router = APIRouter(prefix="/password-reset", tags=["password reset"])

@router.post("/verify-email")
def verify_user_email(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Sprawdza czy istnieje użytkownik ze wszkazanym emailem.
    """
    user_exists = verify_email_exists(db, request.email)
    
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email address does not exist"
        )
    
    return {"email": request.email, "exists": True}

@router.post("/reset")
def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    """
    Zamienia hasło dla użytkownika ze wskazanym emailem.
    """
    success = reset_password_by_email(db, request.email, request.password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to reset password"
        )
    
    return {"message": "Password has been reset successfully"}