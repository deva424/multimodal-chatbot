# Gemini Multimodal Chatbot

A production-grade, asynchronous decoupled chatbot application capable of processing interleaved text and visual asset inputs using unified reasoning cores. The architecture features a lightning-fast **FastAPI backend** handling communication with the Google GenAI SDK and a responsive **Streamlit frontend** interface.

---

## 🏗️ Architecture Overview

The project follows a clean, decoupled service-oriented architecture:
* **Frontend (`app.py`):** Built with Streamlit, handling UI/UX, chat state histories, and multimedia asset staging. It communicates asynchronously with the backend over REST endpoints.
* **Backend (`main.py`):** Built with FastAPI, exposing structured API endpoints (`/api/v1/chat/submit`), enforcing payload validation through Pydantic schemas, and initializing modular AI engine sub-services.
* **Dependency Engine (`uv`):** Utilizing `uv` for ultra-fast package resolution, clean workspace isolation, and reproducible builds using locked deterministic dependencies.

---

## 🛠️ Tech Stack & Ecosystem

* **Language:** Python 3.13+
* **Frontend Engine:** Streamlit
* **Backend Framework:** FastAPI & Uvicorn (ASGI Server)
* **AI Engine:** Google GenAI SDK (`gemini-2.5-flash` or similar reasoning models)
* **Package Manager:** `uv` by Astral

---

## ⚙️ Directory Structure

```text
multimodal-chatbot/
├── .env                  # Local secrets and target host configurations (git-ignored)
├── .gitignore            # Version control tracking exclusions
├── pyproject.toml        # Unified project dependency specifications
├── uv.lock               # Cryptographically locked deterministic environment state
├── app.py                # Streamlit user interface client applicationte
├── main.py               # FastAPI gateway router and entry-point definition
└── src/
    ├── api/
    │   └── v1/
    │       └── endpoints.py   # Versioned API routes and controller endpoints
    ├── schemas/
    │   └── chat.py            # Pydantic data validation structural models
    └── services/
        └── gemini_service.py  # GenAI interface integration wrapper logic

