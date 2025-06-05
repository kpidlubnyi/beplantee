from pydantic import BaseModel, EmailStr, field_validator

class PasswordResetRequest(BaseModel):
    email: EmailStr
    
class PasswordReset(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password')
    def validate_password_requirements(cls, v):
        from app.utils.password_validator import validate_password
        
        validation_result = validate_password(v)
        if not validation_result["valid"]:
            raise ValueError(", ".join(validation_result["errors"]))
        
        return v