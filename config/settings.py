import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    CHAT_MODEL: str = "gemini-3.5-flash"
    IMAGE_MODEL: str = "gemini-3.1-flash-image-preview"
    
    # Cloud Storage Configs
    STORAGE_BUCKET_NAME: str = os.getenv("STORAGE_BUCKET_NAME", "production-chat-assets")

settings = Settings()