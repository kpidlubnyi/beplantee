from sqlalchemy.orm import Session
from app.utils.security import get_password_hash
from app.services.auth_service import get_user_by_email

def verify_email_exists(db: Session, email: str) -> bool:
    """
    Перевіряє, чи існує користувач із вказаною електронною поштою.
    """
    user = get_user_by_email(db, email)
    return user is not None

def reset_password_by_email(db: Session, email: str, new_password: str) -> bool:
    """
    Змінює пароль для користувача з вказаною електронною поштою.
    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return True