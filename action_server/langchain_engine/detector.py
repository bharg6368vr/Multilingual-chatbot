import re
from typing import Dict, Any
from .config import LANGUAGE_NAMES

# Lexicon of distinctive keywords across supported languages
LANGUAGE_KEYWORDS = {
    "en": {
        "what", "how", "why", "when", "where", "who", "which", "can", "could", "would",
        "do", "does", "did", "is", "are", "was", "were", "i", "you", "we", "they",
        "my", "your", "our", "the", "this", "that", "want", "book", "appointment",
        "please", "help", "pricing", "cost", "schedule", "meeting",
        "hello", "hi", "hey", "good", "morning", "afternoon", "evening",
        "thanks", "thank", "bye", "goodbye", "yes", "yeah", "yep", "no", "ok", "okay",
        "service", "services", "support", "hours", "contact", "email", "phone"
    },
    "hi": {
        "namaste", "namaskar", "madad", "dhanyawad", "shukriya", "kripya", "kya", "aap", "meri",
        "kaise", "hain", "alvida", "theek", "shukriyaa", "dost", "samay", "kitna", "keemat", "mulya",
        "seva", "sevayein", "mujhe", "chahiye"
    },
    "es": {
        "hola", "buenos", "dias", "tardes", "noches", "gracias", "servicios", "servicio", "ofrecen",
        "precios", "precio", "cuanto", "cuesta", "costo", "cita", "consulta", "horarios", "horario",
        "por", "favor", "ayuda", "puedo", "estan", "bien", "quienes", "somos"
    },
    "fr": {
        "bonjour", "salut", "merci", "horaires", "horaire", "quels", "quelles", "combien", "cout", "coût",
        "rendez-vous", "aide", "pouvez", "vous", "notre", "votre", "sont", "pourquoi", "comment",
        "tarifs", "tarif", "service", "services", "qui"
    },
    "de": {
        "hallo", "guten", "tag", "morgen", "abend", "danke", "termin", "beratungstermin", "vereinbaren",
        "preise", "kosten", "leistungen", "hilfe", "unterstutzung", "unterstützung", "zeit", "deutsch",
        "kann", "ich", "wie", "viel"
    },
    "it": {
        "ciao", "buongiorno", "buonasera", "grazie", "servizi", "servizio", "prezzo", "prezzi",
        "appuntamento", "aiuto", "favore", "orari", "posso", "quanto", "costa"
    },
    "pt": {
        "ola", "olá", "obrigado", "obrigada", "bom", "dia", "boa", "tarde", "servicos", "serviços",
        "precos", "preços", "agendamento", "ajuda", "posso", "quanto", "custa"
    },
    "kn": {
        "namaskara", "namaskar", "hegiddira", "sahaya", "dhanyavada", "dhanyavadagalu",
        "seve", "sevegalu", "bele", "shulka", "samaya", "yavudu", "beku", "madabahude",
        "elli", "hege", "enu", "kannada", "grahaka"
    }
}

def detect_language(text: str) -> Dict[str, Any]:
    """
    Detects the language of input text with high precision using:
    1. Unicode script ranges (Devanagari, Kannada, Arabic, CJK, Cyrillic)
    2. Distinctive punctuation and keyword matching
    3. Statistical detection with langdetect
    4. Fallback to English
    """
    cleaned = text.strip().lower()
    if not cleaned:
        return {"code": "en", "name": "English", "confidence": 1.0}

    # 1. Distinctive Unicode Script Detection (100% precision)
    if re.search(r"[\u0C80-\u0CFF]", text):
        return {"code": "kn", "name": "Kannada", "confidence": 0.99}
    if re.search(r"[\u0900-\u097F]", text):
        return {"code": "hi", "name": "Hindi", "confidence": 0.99}
    if re.search(r"[\u0600-\u06FF]", text):
        return {"code": "ar", "name": "Arabic", "confidence": 0.99}
    if re.search(r"[\u4E00-\u9FFF]", text):
        return {"code": "zh", "name": "Chinese", "confidence": 0.99}
    if re.search(r"[\u3040-\u309F\u30A0-\u30FF]", text):
        return {"code": "ja", "name": "Japanese", "confidence": 0.99}
    if re.search(r"[\uAC00-\uD7AF]", text):
        return {"code": "ko", "name": "Korean", "confidence": 0.99}
    if re.search(r"[\u0400-\u04FF]", text):
        return {"code": "ru", "name": "Russian", "confidence": 0.99}

    # 2. Distinctive Spanish punctuation
    if "¿" in text or "¡" in text:
        return {"code": "es", "name": "Spanish", "confidence": 0.99}

    # 3. Tokenize words and match against distinctive multilingual lexicons
    words = set(re.findall(r"\b\w+\b", cleaned))
    
    # Priority check: Distinctive non-English keywords first
    non_en_matches = [(lc, len(words & kw)) for lc, kw in LANGUAGE_KEYWORDS.items() if lc != "en" and (words & kw)]
    en_overlap = len(words & LANGUAGE_KEYWORDS["en"])

    if non_en_matches:
        best_non_en, non_en_count = max(non_en_matches, key=lambda x: x[1])
        if non_en_count >= en_overlap:
            return {
                "code": best_non_en,
                "name": LANGUAGE_NAMES.get(best_non_en, best_non_en.upper()),
                "confidence": min(0.98, 0.85 + 0.04 * non_en_count)
            }

    # Check English distinctive words
    if en_overlap >= 1:
        return {
            "code": "en",
            "name": "English",
            "confidence": min(0.98, 0.85 + 0.04 * en_overlap)
        }

    # 4. Statistical detection using langdetect
    try:
        from langdetect import detect_langs
        predictions = detect_langs(text)
        if predictions:
            best = predictions[0]
            code = best.lang
            confidence = round(best.prob, 3)
            # Only accept supported languages from langdetect if confidence is adequate
            if code in LANGUAGE_NAMES and (confidence >= 0.70 or len(cleaned.split()) >= 3):
                return {
                    "code": code,
                    "name": LANGUAGE_NAMES.get(code, code.upper()),
                    "confidence": confidence
                }
    except Exception:
        pass

    return {"code": "en", "name": "English", "confidence": 0.75}

