# src/schemas/chat.py
import base64
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class MessagePartSchema(BaseModel):
    text: Optional[str] = Field(default=None, description="Textual prompt segment.")
    # Change type from bytes to str to handle the incoming Base64 data from HTTP JSON requests cleanly
    image_bytes: Optional[str] = Field(default=None, description="Base64 encoded image payload string.")
    mime_type: Optional[str] = Field(default=None, description="MIME format verification.")

    @field_validator('mime_type')
    @classmethod
    def validate_mime_type(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            allowed = ["image/jpeg", "image/png", "image/webp"]
            if value.lower() not in allowed:
                raise ValueError(f"Unsupported media format. Allowed extensions: {allowed}")
        return value

    @field_validator('image_bytes')
    @classmethod
    def decode_base64_image(cls, value: Optional[str]) -> Optional[bytes]:
        """Automatically converts the incoming Base64 JSON string back into raw bytes."""
        if value is not None and value.strip():
            try:
                # If the string contains a data URI prefix, strip it out out of caution
                if "," in value:
                    value = value.split(",")[1]
                return base64.b64decode(value)
            except Exception:
                raise ValueError("The provided image asset string is not a valid base64 format.")
        return None

class ChatTurnRequest(BaseModel):
    conversation_id: str = Field(..., description="Unique thread identifier.")
    parts: List[MessagePartSchema] = Field(..., min_items=1)

class ChatTurnResponse(BaseModel):
    conversation_id: str
    role: str = "model"
    text_content: str
    generated_image_urls: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)