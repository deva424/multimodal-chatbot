# main.py
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from your .env file into your system

from src.api.v1.endpoints import router as api_v1_router

app = FastAPI(
    title="Production Multimodal Chatbot Service",
    version="1.0.0",
    description="Production-grade pipeline for handling text and image inputs via Gemini."
)

# Mount the versioned API endpoints router
app.include_router(api_v1_router, prefix="/api/v1")

if __name__ == "__main__":
    # Start the local development server
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)