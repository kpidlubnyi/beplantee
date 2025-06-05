from pydantic import BaseModel, EmailStr, field_validator, Field
import re
from typing import List
from app.utils.password_validator import validate_password

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password_requirements(cls, v):
        validation_result = validate_password(v)
        if not validation_result["valid"]:
            raise ValueError(", ".join(validation_result["errors"]))
        
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordValidationError(BaseModel):
    errors: List[str]

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True