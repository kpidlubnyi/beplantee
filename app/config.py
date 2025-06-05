from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "beplantee")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    UPLOAD_DIRECTORY: str = os.getenv("UPLOAD_DIRECTORY", "uploads")

settings = Settings()