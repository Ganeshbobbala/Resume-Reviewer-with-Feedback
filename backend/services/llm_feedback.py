import re
import logging
from typing import Dict, Any, List, Optional

from services.schemas import LLMFeedbackResponse
from services.llm_provider import get_llm_provider
from services.rag_service import get_rag_guidance_for_review
from services.supabase_service import redact_pii

logger = logging.getLogger("llm_feedback")

def extract_resume_bullets(text: str) -> List[str]:
    """Extracts bullet lines or action statements from resume text."""
    lines = text.splitlines()
    bullets = []
    for line in lines:
        cleaned = line.strip().lstrip("•-*–+0123456789.) ").strip()
        if 20 <= len(cleaned) <= 300:
            # Check if line looks like an accomplishment or experience item
            if re.match(r'^(developed|built|engineered|architected|designed|implemented|optimized|scaled|managed|led|created|worked|assisted)', cleaned, re.IGNORECASE):
                bullets.append(cleaned)
    if not bullets:
        # Fallback to lines with reasonable length
        bullets = [ln.strip() for ln in lines if 30 <= len(ln.strip()) <= 200][:3]
    return bullets[:5]

def generate_enhanced_llm_feedback(
    raw_text: str,
    target_role: str,
    detected_skills: List[str],
    matched_skills: List[str],
    missing_skills: List[str],
    demonstrated_skills: Optional[List[str]] = None,
    insufficiently_demonstrated: Optional[List[str]] = None,
    sections: Optional[Dict[str, bool]] = None,
    scores: Optional[Dict[str, Any]] = None,
    provider_type: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Coordinates LLM provider, RAG citations, and deterministic fallbacks
    to produce strictly validated, evidence-backed feedback without hallucinations.
    """
    # 1. PII Redaction
    sanitized_text = redact_pii(raw_text)

    # 2. Extract representative bullets for before-and-after rewrites
    bullets = extract_resume_bullets(sanitized_text)

    # 3. Retrieve relevant RAG career guidance
    has_metrics = bool(re.search(r'\b\d+(?:%|\+|\s*k|\s*m)?\b', raw_text.lower()))
    rag_citations = get_rag_guidance_for_review(
        target_role=target_role,
        missing_skills=missing_skills,
        has_metrics=has_metrics
    )

    # 4. Prepare structured prompt payload
    prompt_data = {
        "target_role": target_role,
        "detected_skills": detected_skills[:15],
        "matched_skills": matched_skills[:10],
        "missing_skills": missing_skills[:6],
        "demonstrated_skills": demonstrated_skills or [],
        "insufficiently_demonstrated": insufficiently_demonstrated or [],
        "sections": sections or {},
        "bullets": bullets,
        "rag_citations": rag_citations
    }

    # 5. Call LLM provider
    provider = get_llm_provider(provider_type=provider_type, api_key=api_key)
    try:
        raw_result = provider.generate_feedback(prompt_data)
        validated = LLMFeedbackResponse(**raw_result)
        return validated.model_dump()
    except Exception as e:
        logger.error(f"Error during LLM feedback generation/validation ({e}). Using rule-based fallback.")
        from services.llm_provider import RuleBasedLLMProvider
        fallback_res = RuleBasedLLMProvider().generate_feedback(prompt_data)
        return fallback_res

