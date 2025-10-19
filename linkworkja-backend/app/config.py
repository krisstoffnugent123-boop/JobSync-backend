from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache
from typing import List
import os

class Settings(BaseSettings):
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Firebase
    firebase_credentials_path: str = "./dev-firebase-credentials.json"
    firebase_database_url: str = "https://linkworkja-dev.firebaseio.com"
    
    # Google AI
    google_ai_api_key: str = "dev-google-ai-key"
    
    # Security
    secret_key: str = "dev-secret-key-not-for-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    model_config = ConfigDict(
        env_file="dev.env" if os.path.exists("dev.env") else None,
        env_file_encoding="utf-8"
    )

@lru_cache()
def get_settings():
    return Settings()