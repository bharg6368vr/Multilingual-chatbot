import os
import sys
import uuid
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

# Ensure action_server is importable for fast local detection
project_root = Path(__file__).resolve().parent.parent
action_server_dir = project_root / "action_server"
if str(action_server_dir) not in sys.path:
    sys.path.insert(0, str(action_server_dir))

try:
    from langchain_engine.detector import detect_language
except Exception:
    def detect_language(text):
        return {"code": "en", "name": "English", "confidence": 1.0}

load_dotenv(dotenv_path=project_root / ".env")

RASA_URL = os.getenv("RASA_SERVER_URL", "http://localhost:5005")
ACTION_URL = os.getenv("ACTION_SERVER_URL", "http://localhost:5055")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").capitalize()

# Flag and language mapping
LANG_FLAGS = {
    "en": ("🇺🇸", "English"),
    "es": ("🇪🇸", "Spanish"),
    "fr": ("🇫🇷", "French"),
    "de": ("🇩🇪", "German"),
    "hi": ("🇮🇳", "Hindi"),
    "kn": ("🇮🇳", "Kannada"),
    "it": ("🇮🇹", "Italian"),
    "pt": ("🇵🇹", "Portuguese"),
    "ru": ("🇷🇺", "Russian"),
    "zh": ("🇨🇳", "Chinese"),
    "ja": ("🇯🇵", "Japanese"),
    "ar": ("🇸🇦", "Arabic")
}

st.set_page_config(
    page_title="Multilingual AI Assistant (Rasa + LangChain)",
    page_icon="🌐",
    layout="wide"
)

# Initialize session states
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 **Hello! Welcome to our Enterprise Multilingual AI Assistant.**\n\nI combine **Rasa Open Source** (deterministic dialogue & slot extraction) with **LangChain** (multilingual LLM orchestration & RAG).\n\nYou can chat with me in **English, Kannada (ಕನ್ನಡ), Hindi, Spanish, French, German, Italian, Portuguese, Arabic, or any other language**!",
            "lang_badge": None
        }
    ]

# Sidebar configuration and diagnostics
with st.sidebar:
    st.title("🌐 System Status")
    
    # Health checks
    def check_health(url):
        try:
            r = requests.get(url, timeout=1.5)
            return r.status_code == 200
        except Exception:
            return False

    rasa_online = check_health(f"{RASA_URL}/")
    action_online = check_health(f"{ACTION_URL}/health")

    col1, col2 = st.columns(2)
    with col1:
        if rasa_online:
            st.success("Rasa: Active (5005)")
        else:
            st.error("Rasa: Offline (5005)")
    with col2:
        if action_online:
            st.success("Actions: Active (5055)")
        else:
            st.warning("Actions: Offline (5055)")

    st.info(f"🧠 **LLM Provider:** {LLM_PROVIDER} Gemini (Flash Lite)")

    st.markdown("---")
    st.subheader("💡 Presentation Demo Prompts")
    quick_prompts = [
        ("🇪🇸 Spanish FAQ & Pricing", "¿Qué servicios ofrecen y cuáles son sus precios?"),
        ("🇫🇷 French Support Hours", "Quels sont vos horaires de support client ?"),
        ("🇮🇳 Hindi Greeting & Help", "Namaste, kya aap meri madad kar sakte hain?"),
        ("🇩🇪 German Consultation", "Kann ich einen Beratungstermin für Cloud vereinbaren?"),
        ("🇺🇸 Appointment Booking", "I want to book an appointment for AI Consulting"),
        ("🇮🇹 Italian Inquiry", "Quali servizi offrite e come posso contattarvi?")
    ]

    for label, prompt_text in quick_prompts:
        if st.button(label, use_container_width=True):
            st.session_state.quick_input = prompt_text
            st.rerun()

    st.markdown("---")
    with st.expander("🏗️ Architecture Overview"):
        st.markdown("""
        **Hybrid Conversational Flow:**
        1. **User Input** in any language.
        2. **Language Detector** analyzes script & distinctive lexicons.
        3. **Rasa Dialogue Manager** handles high-confidence intents & slot forms (e.g. Appointment Booking).
        4. **LangChain Fallback & RAG** handles knowledge queries & localized synthesis via Google Gemini.
        """)

    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversation restarted. How can I help you today?",
                "lang_badge": None
            }
        ]
        st.rerun()

# Main Chat View
st.title("🌐 Multilingual Chatbot (Rasa + LangChain)")
st.caption("🚀 Enterprise Hybrid Architecture: Rasa Open Source (NLU & State Tracking) + LangChain (Multilingual RAG & LLM Orchestration)")

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("lang_badge"):
            st.caption(msg["lang_badge"])
        st.markdown(msg["content"])

# Handle quick button inputs or user chat input
prompt = st.chat_input("Type your message in any language...")
if "quick_input" in st.session_state and st.session_state.quick_input:
    prompt = st.session_state.quick_input
    del st.session_state.quick_input

if prompt:
    # 1. Detect language for visual feedback
    detection = detect_language(prompt)
    detected_code = detection["code"]
    detected_name = detection["name"]
    confidence_pct = int(detection["confidence"] * 100)
    flag, _ = LANG_FLAGS.get(detected_code, ("🌐", detected_name))
    badge_text = f"{flag} **Detected Language:** {detected_name} ({detected_code.upper()}) • **Confidence:** {confidence_pct}%"

    # Append user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "lang_badge": badge_text
    })
    with st.chat_message("user"):
        st.caption(badge_text)
        st.markdown(prompt)

    # 2. Send to Rasa REST API
    with st.chat_message("assistant"):
        with st.spinner("Processing through Rasa & LangChain..."):
            endpoint = f"{RASA_URL}/webhooks/rest/webhook"
            payload = {
                "sender": st.session_state.session_id,
                "message": prompt
            }
            
            try:
                response = requests.post(endpoint, json=payload, timeout=25)
                if response.status_code == 200:
                    bot_responses = response.json()
                    if bot_responses:
                        for bot_msg in bot_responses:
                            text_reply = bot_msg.get("text", "")
                            if text_reply:
                                st.markdown(text_reply)
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": text_reply,
                                    "lang_badge": None
                                })
                    else:
                        fallback_msg = "Received empty response from dialogue agent."
                        st.markdown(fallback_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": fallback_msg,
                            "lang_badge": None
                        })
                else:
                    err_msg = f"⚠️ Server Error ({response.status_code}): {response.text}"
                    st.error(err_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": err_msg,
                        "lang_badge": None
                    })
            except requests.exceptions.ConnectionError:
                offline_msg = (
                    "⚠️ **Cannot connect to Rasa server on port 5005.**\n\n"
                    "Please ensure Rasa and the Action Server are running:\n"
                    "1. Start Action Server: `.\\run_action_server.ps1`\n"
                    "2. Start Rasa Core: `.\\run_rasa.ps1`\n"
                    "Or use `start_all.bat` to launch all services together."
                )
                st.warning(offline_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": offline_msg,
                    "lang_badge": None
                })
            except Exception as e:
                err_msg = f"An unexpected error occurred: {str(e)}"
                st.error(err_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": err_msg,
                    "lang_badge": None
                })
