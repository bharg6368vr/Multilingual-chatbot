import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from langchain_engine.detector import detect_language
from langchain_engine.translator import translate_text
from langchain_engine.rag_engine import get_rag_engine

logger = logging.getLogger(__name__)

class ActionLangChainFallback(Action):
    """
    Rasa Fallback Action delegating out-of-scope, complex, or unhandled
    multilingual queries to LangChain Multilingual RAG & LLM Engine.
    """

    def name(self) -> Text:
        return "action_langchain_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "")
        current_slot_lang = tracker.get_slot("user_language")

        # 1. Detect language
        detection_result = detect_language(user_message)
        detected_lang_code = detection_result["code"]
        detected_lang_name = detection_result["name"]

        # Use detected language or fallback to previously saved slot
        target_lang = detected_lang_code or current_slot_lang or "en"
        logger.info(f"Fallback triggered for '{user_message}' | Detected: {detected_lang_name} ({target_lang})")

        # 2. Invoke LangChain Multilingual RAG Engine
        rag_engine = get_rag_engine()
        response_text = rag_engine.answer_query(
            query=user_message,
            target_lang_code=target_lang
        )

        # 3. Dispatch response back to user
        dispatcher.utter_message(text=response_text)

        # 4. Save detected language into slot for subsequent turns
        return [
            SlotSet("user_language", target_lang)
        ]


class ActionDetectUserLanguage(Action):
    """
    Custom action to explicitly analyze and update the user's language preference.
    """

    def name(self) -> Text:
        return "action_detect_user_language"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "")
        detection = detect_language(user_message)
        lang_code = detection["code"]
        lang_name = detection["name"]

        ack = f"Language detected: {lang_name} ({lang_code})."
        dispatcher.utter_message(text=ack)

        return [SlotSet("user_language", lang_code)]


class ActionMultilingualGreet(Action):
    """
    Greets the user dynamically in their detected or preferred language.
    """

    def name(self) -> Text:
        return "action_multilingual_greet"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "")
        detection = detect_language(user_message)
        lang_code = detection["code"]

        base_greeting = "Hello! Welcome to our multilingual assistant. How can I help you today?"
        localized_greeting = translate_text(base_greeting, target_lang_code=lang_code)

        dispatcher.utter_message(text=localized_greeting)
        return [SlotSet("user_language", lang_code)]
