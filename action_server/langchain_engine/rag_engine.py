import os
from pathlib import Path
from typing import List, Dict, Any

from .config import get_llm, LANGUAGE_NAMES
from .prompt_templates import RAG_MULTILINGUAL_PROMPT

KB_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"

class MultilingualRAGEngine:
    def __init__(self):
        self.llm = get_llm()
        self.documents = []
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Loads all raw text and markdown documents from knowledge_base directory."""
        if not KB_DIR.exists():
            return

        for file_path in KB_DIR.glob("*.*"):
            if file_path.suffix.lower() in [".txt", ".md"]:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        self.documents.append({
                            "source": file_path.name,
                            "content": content
                        })
                except Exception as e:
                    print(f"[RAG Warning] Could not read {file_path}: {e}")

    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> str:
        """
        Retrieves relevant sections from the knowledge base.
        If the entire knowledge base is compact (e.g., standard FAQ documents),
        provides the full context to ensure multilingual inquiries have complete
        access to services, pricing, support hours, and booking policies.
        """
        if not self.documents:
            return "No knowledge base documents currently available."

        combined_text = "\n\n".join([doc["content"] for doc in self.documents])
        
        # When knowledge base is within LLM context size (< 15,000 chars),
        # return entire context so multilingual queries have 100% complete coverage
        if len(combined_text) <= 15000:
            return combined_text

        # Split into distinct sections by headers for larger corpora
        sections = combined_text.split("## ")
        scored_sections = []
        
        query_words = set(query.lower().split())
        for section in sections:
            if not section.strip():
                continue
            section_lower = section.lower()
            score = sum(1 for w in query_words if len(w) > 3 and w in section_lower)
            scored_sections.append((score, section))

        scored_sections.sort(key=lambda x: x[0], reverse=True)
        top_sections = [sec for _, sec in scored_sections[:top_k]]
        return "\n\n## ".join(top_sections)

    def answer_query(self, query: str, target_lang_code: str = "en") -> str:
        """
        Queries the knowledge base and generates an answer in the target language.
        """
        target_lang_name = LANGUAGE_NAMES.get(target_lang_code, "English")
        context = self.retrieve_relevant_context(query)

        try:
            chain = RAG_MULTILINGUAL_PROMPT | self.llm
            response = chain.invoke({
                "context": context,
                "question": query,
                "target_language": target_lang_name,
                "target_language_code": target_lang_code
            })
            return response.content.strip()
        except Exception as e:
            print(f"[RAG Error] Failed to generate response with LangChain: {e}")
            return (
                f"I found the following information in our knowledge base:\n\n{context[:300]}..."
            )

# Global singleton instance
_rag_engine = None

def get_rag_engine() -> MultilingualRAGEngine:
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = MultilingualRAGEngine()
    return _rag_engine
