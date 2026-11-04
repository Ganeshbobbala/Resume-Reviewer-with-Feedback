import os
import re
import json
import logging
from typing import List, Dict, Any, Optional
import numpy as np

from services.semantic_matcher import embedding_service
from services.text_processor import preprocess_text

logger = logging.getLogger("rag_service")

# Prompt injection and malicious override filter patterns
INJECTION_PATTERNS = [
    re.compile(r'ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions', re.IGNORECASE),
    re.compile(r'disregard\s+(?:all\s+)?(?:system|rules)', re.IGNORECASE),
    re.compile(r'you\s+are\s+now\s+(?:an?\s+)?unrestricted', re.IGNORECASE),
    re.compile(r'system\s*:\s*', re.IGNORECASE),
    re.compile(r'<script.*?>.*?</script>', re.IGNORECASE | re.DOTALL),
    re.compile(r'sudo\s+make\s+me', re.IGNORECASE),
]

def sanitize_untrusted_query(query: str) -> str:
    """
    Cleans user queries, job descriptions, or resume excerpts to defuse
    prompt injection attempts and script tags.
    """
    if not query:
        return ""
    clean = query
    for pat in INJECTION_PATTERNS:
        clean = pat.sub("[DEFUSED_INSTRUCTION]", clean)
    # Remove excessive whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:1000]

class RAGKnowledgeEngine:
    """
    Modular Retrieval-Augmented Generation service providing grounded,
    evidence-backed resume advice from curated career and hiring rubrics.
    """
    def __init__(self, knowledge_path: Optional[str] = None):
        if knowledge_path is None:
            backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            knowledge_path = os.path.join(backend_dir, "data", "rag_knowledge", "career_knowledge.json")
        self.knowledge_path = knowledge_path
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None
        self._is_indexed = False
        self.load_and_index()

    def load_and_index(self):
        """Loads curated documents and indexes dense vector representations."""
        if not os.path.exists(self.knowledge_path):
            logger.warning(f"RAG knowledge file not found at {self.knowledge_path}. RAG will operate with empty corpus.")
            self.documents = []
            self._is_indexed = True
            return

        try:
            with open(self.knowledge_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)

            logger.info(f"Loaded {len(self.documents)} RAG knowledge documents.")
            contents = [f"{d['title']} - {d['section']}: {d['content']}" for d in self.documents]
            self.embeddings = embedding_service.encode(contents)
            self._is_indexed = True
            logger.info("RAG vector index generated successfully.")
        except Exception as e:
            logger.error(f"Error indexing RAG knowledge: {e}")
            self.documents = []
            self._is_indexed = True

    def retrieve(
        self,
        query: str,
        target_role: Optional[str] = None,
        top_k: int = 2,
        relevance_threshold: float = 0.35
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top-k relevant knowledge passages with strict relevance thresholding.
        Returns empty list if query is irrelevant or below threshold.
        """
        if not self.documents or self.embeddings is None:
            return []

        clean_query = sanitize_untrusted_query(query)
        if not clean_query:
            return []

        # Enhance query with role context if available
        search_query = f"{target_role}: {clean_query}" if target_role else clean_query
        q_vec = embedding_service.encode([search_query])[0]

        # Cosine similarity
        sims = np.dot(self.embeddings, q_vec)

        # Keyword overlap boost for hybrid retrieval
        query_words = set(preprocess_text(search_query).split())
        results = []

        for idx, doc in enumerate(self.documents):
            dense_sim = float(sims[idx])

            # Lexical overlap
            doc_words = set(preprocess_text(f"{doc['title']} {doc['section']} {doc['content']}").split())
            overlap = len(query_words.intersection(doc_words)) / max(1, len(query_words))
            hybrid_score = (dense_sim * 0.70) + (min(1.0, overlap) * 0.30)

            if hybrid_score >= relevance_threshold:
                results.append({
                    "source_id": doc.get("source_id", "career_guide"),
                    "title": doc.get("title", ""),
                    "section": doc.get("section", ""),
                    "relevance_score": round(hybrid_score, 3),
                    "content": doc.get("content", ""),
                    "tags": doc.get("tags", [])
                })

        # Sort by hybrid relevance score descending
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]

# Global singleton RAG engine
rag_engine = RAGKnowledgeEngine()

def get_rag_guidance_for_review(
    target_role: str,
    missing_skills: List[str],
    has_metrics: bool = False
) -> List[Dict[str, Any]]:
    """
    Retrieves grounded recommendations specifically tailored to candidate's identified gaps.
    """
    guidance = []

    # 1. Action verb and quantification guidance if metrics missing
    if not has_metrics:
        res = rag_engine.retrieve("How to quantify accomplishments with numbers and metrics on resume", target_role=target_role, top_k=1)
        if res:
            guidance.extend(res)

    # 2. Role-specific engineering rubric
    role_res = rag_engine.retrieve(f"{target_role} best practices and required competencies", target_role=target_role, top_k=1)
    if role_res:
        guidance.extend(role_res)

    # Deduplicate citations by title & section
    seen = set()
    deduped = []
    for g in guidance:
        key = (g["title"], g["section"])
        if key not in seen:
            seen.add(key)
            deduped.append(g)

    return deduped

