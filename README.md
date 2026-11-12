# 🌐 Multilingual AI Chatbot (Rasa + LangChain)

An enterprise-grade conversational AI architecture combining **Rasa Open Source** (deterministic dialogue management, state tracking, intent/slot extraction) and **LangChain** (multilingual LLM orchestration, dynamic language detection, real-time translation, and multilingual RAG).

---

## 🏗️ Architecture Overview

The system implements a **Hybrid Conversational Architecture**:

```
[ User Input in Any Language ]
             │
             ▼
      [ Streamlit Web UI ] (Port 8501)
             │  (REST API)
             ▼
     [ Rasa Core & NLU ] (Port 5005)
             │
   ┌─────────┴─────────┐
   │ High Confidence   │ Low Confidence / Fallback / Knowledge Query
   ▼                   ▼
[ Rasa Dialog ]   [ Rasa Action Server ] (Port 5055)
(Forms/Stories)        │
                       ▼
                 [ LangChain Engine ]
                 ├── 1. Language Detector (langdetect + heuristic)
                 ├── 2. Multilingual Knowledge Base (RAG)
                 ├── 3. LLM Orchestrator (Google Gemini / OpenAI)
                 └── 4. Real-time Response Translator
                       │
                       ▼
            [ Localized Final Reply ]
```

1. **Rasa Dialogue Manager**: Manages rule-based responses, entity slot-filling (e.g., booking appointments, collecting contact info), and state tracking.
2. **LangChain Fallback Engine**: When Rasa detects an open-domain question, FAQ inquiry, or out-of-scope intent, it delegates to the LangChain engine via `action_langchain_fallback`.
3. **Language Detection & Adaptation**: The system automatically detects the user's input language (Spanish, French, Hindi, German, Arabic, etc.), retrieves relevant knowledge base context, and crafts the answer directly in the user's native language.

---

## 📂 Project Structure

```
multilingual-chatbot/
│
├── .env.example                 # Environment configuration template
├── requirements.txt             # Python dependencies
│
├── rasa_bot/                    # Rasa Dialogue Engine
│   ├── config.yml               # NLU pipeline & fallback classifier settings
│   ├── domain.yml               # Intents, entities, slots, and actions
│   ├── credentials.yml          # REST channel connector
│   ├── endpoints.yml            # Action server endpoint (http://localhost:5055)
│   └── data/
│       ├── nlu.yml              # Intent training data with multilingual examples
│       ├── rules.yml            # Deterministic fallback & dialogue rules
│       └── stories.yml          # Interactive conversational stories
│
├── action_server/               # Rasa Custom Actions + LangChain Integration
│   ├── actions.py               # ActionLangChainFallback & ActionMultilingualGreet
│   ├── langchain_engine/
│   │   ├── config.py            # LLM provider factory (Gemini, OpenAI, Mock)
│   │   ├── detector.py          # Fast language detection module
│   │   ├── translator.py        # Real-time translation chain
│   │   ├── rag_engine.py        # Multilingual knowledge base retrieval (RAG)
│   │   └── prompt_templates.py  # Localized prompt templates
│   └── knowledge_base/
│       └── company_info.txt     # Sample enterprise knowledge base
│
├── frontend/
│   └── app.py                   # Streamlit interactive chat UI with language badges
│
├── setup_env.ps1                # Automated Python 3.10 & virtual environment setup
├── train_bot.ps1                # Script to train Rasa model
├── run_action_server.ps1        # Script to start action server
├── run_rasa.ps1                 # Script to start Rasa core server
├── run_frontend.ps1             # Script to launch Streamlit UI
└── start_all.bat                # One-click launcher for all services
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites (Python 3.10)
> [!IMPORTANT]
> Rasa Open Source 3.x requires **Python 3.8, 3.9, or 3.10**. 

If you do not have Python 3.10 installed, run:
```powershell
winget install Python.Python.3.10
```

### 2. Environment Setup
Run the automated setup script to create your virtual environment and install all dependencies:
```powershell
.\setup_env.ps1
```

Or manually:
```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

### 3. Configure API Keys
Edit `.env` and set your preferred LLM provider:
```env
LLM_PROVIDER=google
GOOGLE_API_KEY=your_gemini_api_key_here
```
*(Note: If no API key is provided, the system defaults to a built-in local mock LLM for offline testing).*

### 4. Train the Rasa Model
Train the dialogue and NLU model:
```powershell
.\train_bot.ps1
```

### 5. Launch the Chatbot
You can launch all services in separate windows using:
```cmd
start_all.bat
```

Or run each service in separate terminals:
- **Terminal 1 (Action Server)**: `.\run_action_server.ps1`
- **Terminal 2 (Rasa Core)**: `.\run_rasa.ps1`
- **Terminal 3 (Web UI)**: `.\run_frontend.ps1`

Open your browser at **`http://localhost:8501`** to chat with the assistant!

---

## 🧪 Testing Multilingual Scenarios

Try the following prompts to observe the hybrid behavior:

| Language | Query | Handling Component | Expected Behavior |
| :--- | :--- | :--- | :--- |
| 🇪🇸 **Spanish** | `¿Qué servicios ofrecen y cuáles son sus precios?` | LangChain RAG Fallback | Answers about pricing from knowledge base in Spanish |
| 🇫🇷 **French** | `Quels sont vos horaires de support client ?` | LangChain RAG Fallback | Answers support hours (24/7/365) in French |
| 🇮🇳 **Hindi** | `Namaste, kya aap meri madad kar sakte hain?` | Rasa / Action Server | Welcomes user in Hindi |
| 🇺🇸 **English** | `I want to book an appointment for AI Consulting` | Rasa Core Form / Story | Guides the user through slot-filling (name & service) |
| 🇩🇪 **German** | `Kann ich einen Beratungstermin für Cloud vereinbaren?` | LangChain / Rasa Fallback | Synthesizes response in German |
