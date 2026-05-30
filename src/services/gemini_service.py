import io
import logging
from typing import List, Any, Tuple
from PIL import Image
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config.settings import settings
from src.schemas.chat import MessagePartSchema

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client = genai.Client()

    def process_incoming_parts(self, request_parts: List[MessagePartSchema]) -> List[Any]:
        sdk_contents = []
        for idx, part in enumerate(request_parts):
            if part.text and part.text.strip():
                sdk_contents.append(part.text)
            
            if part.image_bytes:
                try:
                    img = Image.open(io.BytesIO(part.image_bytes))
                    img.verify()
                    img = Image.open(io.BytesIO(part.image_bytes))
                    sdk_contents.append(img)
                except Exception as e:
                    logger.error(f"Corrupted image payload dropped at index {idx}: {str(e)}")
                    raise ValueError(f"Invalid image content at index {idx}.")
        return sdk_contents

    def execute_turn(self, history: List[Any], new_request_parts: List[MessagePartSchema]) -> Tuple[str, List[Image.Image]]:
        try:
            new_sdk_inputs = self.process_incoming_parts(new_request_parts)
            full_contents = history + new_sdk_inputs

            response = self.client.models.generate_content(
                model=settings.CHAT_MODEL,
                contents=full_contents
            )

            text_output = ""
            generated_images = []

            if response.parts:
                for part in response.parts:
                    if part.text is not None:
                        text_output += part.text
                    elif part.inline_data is not None:
                        generated_images.append(part.as_image())

            return text_output, generated_images

        except APIError as api_err:
            logger.error(f"Gemini API Failure: {api_err.message}")
            raise RuntimeError(f"Model Inference Error: {api_err.message}")