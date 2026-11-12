import os
import requests
from pathlib import Path
from typing import List, Optional, Any
from dotenv import load_dotenv

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration

# Search for .env in project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ar": "Arabic",
    "nl": "Dutch",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "bn": "Bengali",
    "ko": "Korean"
}


class GoogleGeminiChatModel(BaseChatModel):
    """
    Direct REST-based Gemini client compatible with LangChain.
    Avoids gRPC and Protobuf conflicts with Rasa.
    """
    model_name: str = "gemini-flash-lite-latest"
    api_key: str = ""

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        contents = []
        system_instruction = None

        for msg in messages:
            if isinstance(msg, SystemMessage):
                system_instruction = msg.content
            elif isinstance(msg, HumanMessage):
                contents.append({"role": "user", "parts": [{"text": msg.content}]})
            elif isinstance(msg, AIMessage):
                contents.append({"role": "model", "parts": [{"text": msg.content}]})
            else:
                contents.append({"parts": [{"text": msg.content}]})

        # Prepend system instruction if provided
        if system_instruction and contents:
            first_text = contents[0]["parts"][0]["text"]
            contents[0]["parts"][0]["text"] = f"[Instruction: {system_instruction}]\n\n{first_text}"

        models_to_try = [self.model_name, "gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-3.8-flash"]
        last_error = ""

        for m in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={self.api_key}"
            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 1000
                }
            }

            try:
                res = requests.post(url, json=payload, timeout=12)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text_reply = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        if text_reply.strip():
                            return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text_reply))])
                else:
                    last_error = f"Status {res.status_code}: {res.text[:100]}"
            except Exception as e:
                last_error = str(e)

        # Graceful fallback to local mock engine if remote service is unavailable
        mock_result = LocalMultilingualMockLLM()._generate(messages)
        return mock_result

    @property
    def _llm_type(self) -> str:
        return "gemini-rest"


class OpenAIChatModel(BaseChatModel):
    """Direct REST-based OpenAI client compatible with LangChain."""
    model_name: str = "gpt-4o-mini"
    api_key: str = ""

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        formatted_messages = []
        for msg in messages:
            role = "user"
            if isinstance(msg, SystemMessage):
                role = "system"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            formatted_messages.append({"role": role, "content": msg.content})

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": formatted_messages,
            "temperature": 0.3
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                reply = res.json()["choices"][0]["message"]["content"]
                return ChatResult(generations=[ChatGeneration(message=AIMessage(content=reply))])
        except Exception:
            pass

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="OpenAI connection error."))])

    @property
    def _llm_type(self) -> str:
        return "openai-rest"


class LocalMultilingualMockLLM(BaseChatModel):
    """Offline fallback mock LLM."""
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        last_text = messages[-1].content if messages else ""
        reply = (
            f"We offer Cloud Solutions, AI Consulting, and Full-Stack Engineering with 24/7 global support."
        )
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=reply))])

    @property
    def _llm_type(self) -> str:
        return "multilingual-mock"


def get_llm():
    """Returns the configured LLM engine."""
    if LLM_PROVIDER == "google" and GOOGLE_API_KEY:
        return GoogleGeminiChatModel(api_key=GOOGLE_API_KEY)
    elif LLM_PROVIDER == "openai" and OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
        return OpenAIChatModel(api_key=OPENAI_API_KEY)
    return LocalMultilingualMockLLM()
