from .config import get_llm, LANGUAGE_NAMES
from .prompt_templates import TRANSLATION_PROMPT

def translate_text(text: str, target_lang_code: str) -> str:
    """
    Translates text into the target language using LangChain LLM.
    """
    if not text or target_lang_code == "en":
        return text

    target_language_name = LANGUAGE_NAMES.get(target_lang_code, target_lang_code)

    try:
        llm = get_llm()
        chain = TRANSLATION_PROMPT | llm
        response = chain.invoke({
            "target_language": target_language_name,
            "text": text
        })
        return response.content.strip()
    except Exception as e:
        print(f"[Translation Warning] LangChain translation failed: {e}")
        # Secondary fallback using googletrans if installed
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, dest=target_lang_code)
            return result.text
        except Exception:
            return text
