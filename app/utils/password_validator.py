import re

def validate_password(password: str) -> dict:
    """
    Перевіряє пароль на відповідність критеріям безпеки.
    
    Критерії:
    - Довжина щонайменше 8 символів
    - Містить лише латинські літери, цифри та спецсимволи
    - Має хоча б одну велику літеру
    - Має хоча б одну маленьку літеру
    - Має хоча б одну цифру
    - Має хоча б один спеціальний символ
    
    Повертає словник з результатами перевірки:
    {
        "valid": bool,
        "errors": list[str]
    }
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]+$', password):
        errors.append("Password must contain only Latin letters, digits, and special characters")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        errors.append("Password must contain at least one special character")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }