from fastapi import APIRouter, Body
from app.schemas.auth import PasswordValidationError
from app.utils.password_validator import validate_password

router = APIRouter(prefix="/password-validation", tags=["password validation"])

@router.post("/", response_model=PasswordValidationError)
def validate_password_strength(password: str = Body(...)):
    """
    Перевіряє силу пароля відповідно до критеріїв безпеки.
    Повертає список помилок, якщо пароль не відповідає критеріям.
    Порожній список означає, що пароль валідний.
    """
    validation_result = validate_password(password)
    return {"errors": validation_result["errors"]}