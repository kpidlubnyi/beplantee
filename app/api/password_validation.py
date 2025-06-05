from fastapi import APIRouter, Body
from app.schemas.auth import PasswordValidationError
from app.utils.password_validator import validate_password

router = APIRouter(prefix="/password-validation", tags=["password validation"])

@router.post("/", response_model=PasswordValidationError)
def validate_password_strength(password: str = Body(...)):
    """
    Sprawdza czy hasło odpowiada standardom bezpieczeństwa.
    Zwraca listę błędów, jeśli hasło nie odpowiada kryteriom.
    Pusta lista oznacza że hasło jest walidne.
    """
    validation_result = validate_password(password)
    return {"errors": validation_result["errors"]}