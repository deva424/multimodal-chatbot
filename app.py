# app.py
import streamlit as st
import requests
import base64
import uuid

# Configuration parameters
API_URL = "http://127.0.0.1:8000/api/v1/chat/submit"

st.set_page_config(
    page_title="Gemini Multimodal Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gemini Multimodal Chatbot")
st.caption("A production-grade pipeline handling text and visual asset reasoning.")

# 1. Initialize Persistent Session States
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    # Keeps track of UI history display list: [{"role": "user"/"assistant", "content": "text", "image": bytes or None}]
    st.session_state.messages = []

# 2. Render Existing Chat Message History Thread
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("image"):
            st.image(message["image"], caption="Uploaded Context Asset", width=300)

# 3. Create the Persistent Bottom Layout Input Component Wrapper
with st.sidebar:
    st.header("Media Attachments")
    uploaded_file = st.file_uploader(
        "Upload contextual image asset...", 
        type=["jpg", "jpeg", "png", "webp"],
        key="image_uploader"
    )
    if uploaded_file:
        st.image(uploaded_file, caption="Staged Image Preview", use_container_width=True)

# 4. Handle Live User Interaction Prompt Input Loop
if user_prompt := st.chat_input("Ask a question or analyze an image..."):
    
    # Render user prompt inside the chat UI container instantly
    with st.chat_message("user"):
        st.markdown(user_prompt)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    # Convert the file bytes to a Base64 string for JSON transit if an image is present
    img_base64 = None
    img_mime = None
    raw_img_bytes_for_ui = None
    
    if uploaded_file:
        raw_img_bytes_for_ui = uploaded_file.getvalue()
        img_base64 = base64.b64encode(raw_img_bytes_for_ui).decode("utf-8")
        img_mime = uploaded_file.type

    # Append user turn data directly to UI memory cache
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt,
        "image": raw_img_bytes_for_ui
    })

    # 5. Package Payload Mapping and Dispatch to FastAPI Layer
    payload = {
        "conversation_id": st.session_state.conversation_id,
        "parts": [
            {
                "text": user_prompt,
                "image_bytes": img_base64,
                "mime_type": img_mime
            }
        ]
    }

    with st.chat_message("assistant"):
        with st.spinner("Analyzing multimodal elements via Gemini Engine..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    response_data = response.json()
                    ai_text = response_data.get("text_content", "")
                    
                    # Render response onto screen view
                    st.markdown(ai_text)
                    
                    # Save assistant response payload token segments back to UI history cache
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_text,
                        "image": None
                    })
                    
                    # Rerun application layout loop to clear sidebar staging area state cleanly
                    st.rerun()
                else:
                    st.error(f"Backend Server returned an error state: (Code {response.status_code})")
                    st.write(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("Connection Interface Dropped. Ensure your FastAPI server (`main.py`) is running on port 8000!")