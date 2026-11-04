import os
import re
import logging
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from services.skill_extractor import extract_skills, SKILL_PATTERNS
from services.text_processor import preprocess_text
from services.job_matcher import STOP_WORDS, extract_keywords, extract_years_experience

logger = logging.getLogger("semantic_matcher")

class DenseEmbeddingService:
    """
    Manages dense text embeddings with lazy loading, caching,
    and automatic lightweight fallback.
    """
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self._model = None
        self._is_loaded = False
        self._fallback_mode = False

    def _load_model(self):
        if self._is_loaded:
            return

        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading SentenceTransformer embedding model: {self.model_name}...")
            self._model = SentenceTransformer(self.model_name)
            self._is_loaded = True
            self._fallback_mode = False
            logger.info("SentenceTransformer loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer ({e}). Falling back to TF-IDF Latent Semantic Embedder.")
            self._fallback_mode = True
            self._is_loaded = True

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encodes a list of texts into dense vectors."""
        self._load_model()
        if not texts:
            return np.zeros((0, 384))

        if not self._fallback_mode and self._model is not None:
            try:
                embeddings = self._model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
                # Normalize L2
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                norms[norms == 0] = 1.0
                return embeddings / norms
            except Exception as e:
                logger.error(f"Error encoding with SentenceTransformer: {e}. Using fallback.")

        # High-performance TF-IDF Latent Semantic Fallback
        return self._fallback_encode(texts)

    def _fallback_encode(self, texts: List[str]) -> np.ndarray:
        """
        Sublinear TF-IDF normalized vector projection fallback.
        Ensures 100% availability even without GPU or network.
        """
        cleaned = [preprocess_text(t) or "empty" for t in texts]
        vec = TfidfVectorizer(ngram_range=(1, 2), max_features=384, sublinear_tf=True)
        try:
            mat = vec.fit_transform(cleaned).toarray()
            norms = np.linalg.norm(mat, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return mat / norms
        except Exception:
            return np.ones((len(texts), 384)) / np.sqrt(384)

# Global singleton embedding service
embedding_service = DenseEmbeddingService()

def chunk_job_requirements(jd_text: str) -> List[str]:
    """
    Parses job description into discrete actionable requirement statements.
    """
    lines = re.split(r'[\r\n]+', jd_text)
    requirements = []

    for line in lines:
        cleaned = line.strip().lstrip("•-*–+0123456789.) ").strip()
        if len(cleaned) < 15:
            continue
        # Split compound sentences if long
        if len(cleaned) > 200:
            subparts = re.split(r'[;.]\s+', cleaned)
            for sp in subparts:
                if len(sp.strip()) >= 15:
                    requirements.append(sp.strip())
        else:
            requirements.append(cleaned)

    # If no line-based requirements extracted, split by sentences
    if not requirements:
        sentences = re.split(r'(?<=[.!?])\s+', jd_text)
        requirements = [s.strip() for s in sentences if len(s.strip()) >= 15]

    return requirements[:20] if requirements else [jd_text[:300]]

def chunk_resume_passages(resume_text: str) -> List[Dict[str, str]]:
    """
    Splits resume into distinct content passages with inferred section context.
    """
    lines = re.split(r'[\r\n]+', resume_text)
    passages = []
    current_section = "General"

    section_keywords = {
        "experience": "Work Experience",
        "project": "Projects",
        "skill": "Technical Skills",
        "education": "Education",
        "summary": "Summary",
        "certif": "Certifications"
    }

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        # Check section header
        lower = line_clean.lower()
        if len(line_clean) < 40:
            for kw, sec_name in section_keywords.items():
                if kw in lower:
                    current_section = sec_name
                    break

        clean_item = line_clean.lstrip("•-*–+0123456789.) ").strip()
        if len(clean_item) >= 20:
            passages.append({
                "text": clean_item,
                "section": current_section
            })

    if not passages:
        passages.append({"text": resume_text[:1000], "section": "General"})

    return passages

def compute_semantic_matching(
    resume_text: str,
    job_description: str,
    semantic_weight: float = 0.50,
    lexical_weight: float = 0.50
) -> Dict[str, Any]:
    """
    Performs comprehensive hybrid resume-to-job matching:
    - Lexical TF-IDF baseline matching
    - Dense semantic vector similarity
    - Evidence extraction for each job requirement
    - Skill verification (does NOT assume candidate has a skill purely from semantic similarity)
    - Fully backward compatible with existing analyze_job_match schema.
    """
    if not job_description or len(job_description.strip()) < 15:
        raise ValueError("Job description is too short or empty.")
    if not resume_text or len(resume_text.strip()) < 15:
        raise ValueError("Resume text is too short or empty.")

    # 1. Lexical baseline metrics (exact preserve of logic from job_matcher.py)
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)
    resume_skills_lower = {s.lower() for s in resume_skills}

    matched_skills = [s for s in jd_skills if s.lower() in resume_skills_lower or any(s.lower() in r for r in resume_skills_lower)]
    missing_skills = [s for s in jd_skills if s not in matched_skills]

    total_jd_skills = len(jd_skills)
    skill_match_score = min(100, round((len(matched_skills) / total_jd_skills) * 100)) if total_jd_skills > 0 else 75

    jd_keywords = extract_keywords(job_description)
    resume_text_lower = resume_text.lower()
    matched_keywords = [kw for kw in jd_keywords if kw.lower() in resume_text_lower]
    missing_keywords = [kw for kw in jd_keywords if kw.lower() not in resume_text_lower]

    keyword_match_score = min(100, round((len(matched_keywords) / min(30, len(jd_keywords))) * 100)) if len(jd_keywords) > 0 else 70

    jd_exp = extract_years_experience(job_description)
    has_exp = bool(re.search(r'\b(experience|worked|developed|engineer|developer|intern)\b', resume_text_lower))
    if jd_exp == "Not specified" or "fresher" in jd_exp.lower() or "entry" in jd_exp.lower():
        experience_match_score = 100
    elif has_exp:
        experience_match_score = 90
    else:
        experience_match_score = 65

    education_terms = ["bachelor", "master", "degree", "b.tech", "m.tech", "computer science", "engineering", "bs", "ms"]
    jd_edu_required = any(term in job_description.lower() for term in education_terms)
    resume_edu_present = any(term in resume_text_lower for term in education_terms)
    education_match_score = 100 if (not jd_edu_required or resume_edu_present) else 60

    # 2. Dense Semantic Matching across Sections & Requirements
    requirements = chunk_job_requirements(job_description)
    passages = chunk_resume_passages(resume_text)
    passage_texts = [p["text"] for p in passages]

    req_embeddings = embedding_service.encode(requirements)
    passage_embeddings = embedding_service.encode(passage_texts)

    # Cosine similarity matrix: (num_requirements, num_passages)
    sim_matrix = np.dot(req_embeddings, passage_embeddings.T)

    requirement_breakdown = []
    semantic_scores_per_req = []

    for i, req in enumerate(requirements):
        best_passage_idx = int(np.argmax(sim_matrix[i]))
        best_sim = float(sim_matrix[i, best_passage_idx])
        normalized_sim = max(0.0, min(1.0, (best_sim + 1.0) / 2.0 if best_sim < 0 else best_sim))
        semantic_scores_per_req.append(normalized_sim)

        best_passage = passages[best_passage_idx]

        # Check explicit keywords / skills inside requirement
        req_skills = extract_skills(req)
        has_skill_proof = any(s.lower() in resume_skills_lower for s in req_skills) if req_skills else True

        # Status: Matched, Partially Demonstrated, or Missing
        if normalized_sim >= 0.70 and has_skill_proof:
            status = "matched"
        elif normalized_sim >= 0.50:
            status = "partially_demonstrated"
        else:
            status = "missing"

        requirement_breakdown.append({
            "requirement": req,
            "status": status,
            "semantic_similarity": round(normalized_sim * 100, 1),
            "supporting_section": best_passage["section"],
            "supporting_excerpt": best_passage["text"][:200] if status != "missing" else "No direct evidence found.",
            "skills_checked": req_skills
        })

    avg_semantic_sim = float(np.mean(semantic_scores_per_req)) if semantic_scores_per_req else 0.7
    dense_semantic_score = min(100, max(20, round(avg_semantic_sim * 100)))

    # Lexical TF-IDF score
    try:
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_mat = tfidf.fit_transform([preprocess_text(resume_text), preprocess_text(job_description)])
        lex_sim = float(cosine_similarity(tfidf_mat[0:1], tfidf_mat[1:2])[0][0])
        lexical_score = min(100, max(30, round(lex_sim * 100 + 40)))
    except Exception:
        lexical_score = 75

    # Hybrid Role Similarity Score
    hybrid_role_similarity = round((dense_semantic_score * semantic_weight) + (lexical_score * lexical_weight))

    # Final Combined Match Score (Preserves baseline balance while incorporating dense semantics)
    final_match_score = round(
        (skill_match_score * 0.35) +
        (hybrid_role_similarity * 0.25) +
        (keyword_match_score * 0.20) +
        (experience_match_score * 0.10) +
        (education_match_score * 0.10)
    )

    # Recommendations
    recommendations = []
    if missing_skills:
        missing_str = ", ".join(missing_skills[:4])
        recommendations.append(f"Highlight hands-on project experience with required skills: {missing_str}.")

    # Highlight any unmet requirements from semantic breakdown
    missing_reqs = [r["requirement"] for r in requirement_breakdown if r["status"] == "missing"]
    if missing_reqs:
        recommendations.append(f"Address key missing job requirement: '{missing_reqs[0]}'.")

    if missing_keywords:
        missing_kw_str = ", ".join(missing_keywords[:4])
        recommendations.append(f"Optimize your resume by incorporating job keywords: {missing_kw_str}.")

    if not re.search(r'\b\d+(?:%|\+|\s*k|\s*m)?\b', resume_text_lower):
        recommendations.append("Add measurable outcomes to your projects (e.g. 'Improved system throughput by 35%').")

    if not recommendations:
        recommendations.append("Your resume aligns strongly with the job description! Ensure key achievements are prominent.")

    return {
        # Baseline compatible keys
        "match_score": final_match_score,
        "skill_match": skill_match_score,
        "keyword_match": keyword_match_score,
        "experience_match": experience_match_score,
        "education_match": education_match_score,
        "role_similarity": hybrid_role_similarity,
        "matched_skills": matched_skills[:15],
        "missing_skills": missing_skills[:15],
        "matched_keywords": matched_keywords[:15],
        "missing_keywords": missing_keywords[:15],
        "recommendations": recommendations,

        # Advanced Semantic Enhancements
        "semantic_score": dense_semantic_score,
        "lexical_score": lexical_score,
        "hybrid_score": hybrid_role_similarity,
        "requirement_breakdown": requirement_breakdown[:10],
        "total_requirements_analyzed": len(requirement_breakdown),
        "matched_requirements_count": sum(1 for r in requirement_breakdown if r["status"] == "matched"),
        "partially_matched_count": sum(1 for r in requirement_breakdown if r["status"] == "partially_demonstrated"),
        "missing_requirements_count": sum(1 for r in requirement_breakdown if r["status"] == "missing"),
        "embedding_mode": "SentenceTransformer" if not embedding_service._fallback_mode else "TF-IDF Latent Semantic"
    }

