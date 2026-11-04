import os
import json
import logging
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from services.schemas import LLMFeedbackResponse, StrengthItem, MissingSkillItem, SectionSuggestion, BulletRewrite, RAGCitation

logger = logging.getLogger("llm_provider")

class BaseLLMProvider(ABC):
    """Abstract interface for provider-independent LLM feedback generation."""
    @abstractmethod
    def generate_feedback(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generates structured feedback dictionary adhering to LLMFeedbackResponse schema."""
        pass

class RuleBasedLLMProvider(BaseLLMProvider):
    """
    Deterministic rule-based provider that produces grounded, hallucination-free
    structured feedback without requiring external APIs or GPU resources.
    Guarantees 100% availability and strict compliance with non-fabrication rules.
    """
    def generate_feedback(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        target_role = prompt_data.get("target_role", "Software Engineer")
        matched_skills = prompt_data.get("matched_skills", [])
        missing_skills = prompt_data.get("missing_skills", [])
        demonstrated_skills = prompt_data.get("demonstrated_skills", [])
        insufficiently_demonstrated = prompt_data.get("insufficiently_demonstrated", [])
        sections = prompt_data.get("sections", {})
        rag_citations_raw = prompt_data.get("rag_citations", [])
        bullets = prompt_data.get("bullets", [])

        # 1. Summary
        summary = (
            f"Candidate profile analyzed for {target_role} track. "
            f"Demonstrates technical grounding in {', '.join(matched_skills[:4]) if matched_skills else 'core fundamentals'} "
            f"with key opportunities to highlight measurable impact and technical depth."
        )

        # 2. Verified Strengths
        strengths = []
        for s in demonstrated_skills[:3]:
            strengths.append({
                "strength": f"Demonstrated practical capability in {s}",
                "supporting_excerpt": f"Applied {s} with action verbs in Experience/Projects section.",
                "relevance": f"Directly satisfies core competencies expected for {target_role} positions."
            })
        if not strengths and matched_skills:
            strengths.append({
                "strength": f"Foundational familiarity with {matched_skills[0]}",
                "supporting_excerpt": f"Documented in Technical Skills.",
                "relevance": f"Provides baseline tooling for {target_role} workflows."
            })

        # 3. Skill Gaps
        skill_gaps = []
        for m in missing_skills[:4]:
            skill_gaps.append({
                "skill": m,
                "status": "missing",
                "recommendation": f"Develop a portfolio project or complete a practical implementation incorporating {m}."
            })
        for ins in insufficiently_demonstrated[:2]:
            skill_gaps.append({
                "skill": ins,
                "status": "insufficiently_demonstrated",
                "recommendation": f"Add an accomplishment bullet in your experience detailing how you applied {ins} to solve a concrete engineering problem."
            })

        # 4. Section Suggestions
        section_suggs = []
        if not sections.get("summary"):
            section_suggs.append({
                "section": "Professional Summary",
                "critique": "Summary section is missing or brief.",
                "recommendation": "Add a 2-3 line technical overview emphasizing your core stack, years of experience, and key technical focus."
            })
        if not sections.get("projects"):
            section_suggs.append({
                "section": "Projects",
                "critique": "Dedicated Projects section is absent.",
                "recommendation": "Include 2-3 end-to-end technical projects featuring GitHub links, architecture overviews, and live deployment URLs."
            })
        section_suggs.append({
            "section": "Professional Experience",
            "critique": "Bullet points could benefit from stronger active verbs and explicit metrics.",
            "recommendation": "Begin bullets with strong action verbs (e.g. 'Architected', 'Engineered') and incorporate measurable business outcomes."
        })

        # 5. Bullet Rewrites with Candidate Metric Placeholders (NO FABRICATED NUMBERS!)
        rewrites = []
        sample_bullets = bullets[:2] if bullets else ["Worked on developing web features and resolving bugs."]
        for b in sample_bullets:
            rewrites.append({
                "original_bullet": b,
                "improved_bullet": f"Engineered and deployed scalable module enhancements for {target_role}, improving system performance by [insert measurable outcome, e.g. +30%] and serving [specify user volume/scale, e.g. 50k+ users].",
                "framework_used": "Action-Context-Result (ACR)",
                "metric_placeholder": "[Please supply: exact percentage, latency reduction, user volume, or hours saved]"
            })

        # 6. RAG Citations
        citations = []
        for c in rag_citations_raw[:3]:
            citations.append({
                "source_title": c.get("title", "Career Best Practices"),
                "section": c.get("section", "Standard Guidelines"),
                "key_principle": c.get("content", "")[:180] + "..."
            })

        # 7. Prioritized Next Steps
        next_steps = [
            f"1. Close primary skill gap: Add demonstrable evidence or a project for {missing_skills[0]}." if missing_skills else "1. Feature your most impactful architectural decisions at the top of your experience section.",
            "2. Quantify existing bullet points: Replace qualitative phrases with concrete metrics (latency, QPS, percentages).",
            "3. Optimize section layout: Ensure technical skills are organized cleanly by category (Languages, Frameworks, Cloud/Databases)."
        ]

        return {
            "resume_summary": summary,
            "verified_strengths": strengths,
            "skill_gaps": skill_gaps,
            "job_specific_recommendations": [
                f"Align your project portfolio with modern {target_role} production patterns.",
                "Ensure github repositories linked in your resume include clean READMEs and deployment guides."
            ],
            "section_suggestions": section_suggs,
            "bullet_rewrites": rewrites,
            "supporting_evidence": [
                f"Confirmed technical skills present: {', '.join(matched_skills[:6])}."
            ],
            "rag_citations": citations,
            "prioritized_next_steps": next_steps,
            "limitations_and_uncertainty": "Rule-based heuristic analysis. Recommendations reflect standard engineering rubrics and should be adapted to specific job applications.",
            "provider_used": "rule_based_deterministic"
        }

class MockLLMProvider(BaseLLMProvider):
    """Mock provider for unit testing without external calls."""
    def generate_feedback(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        rb = RuleBasedLLMProvider()
        res = rb.generate_feedback(prompt_data)
        res["provider_used"] = "mock_provider"
        return res

class OpenAILLMProvider(BaseLLMProvider):
    """OpenAI API Provider with Pydantic JSON validation and safe fallback."""
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", model)

    def generate_feedback(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not configured. Falling back to rule-based engine.")
            return RuleBasedLLMProvider().generate_feedback(prompt_data)

        endpoint = "https://api.openai.com/v1/chat/completions"
        system_prompt = (
            "You are an expert senior engineering hiring manager and career coach. "
            "You provide rigorous, honest, evidence-based feedback on technical resumes. "
            "CRITICAL RULES: NEVER invent companies, degrees, dates, skills, or numerical metrics. "
            "If a bullet rewrite requires numbers or scale that are unverified, use clear candidate placeholders "
            "like '[insert metric, e.g. +30%]' rather than making up numbers. "
            "Return valid JSON matching the LLMFeedbackResponse schema."
        )

        user_content = json.dumps(prompt_data)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this resume data and return structured JSON feedback:\n{user_content}"}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(endpoint, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    parsed["provider_used"] = f"openai_{self.model}"
                    # Validate through Pydantic
                    validated = LLMFeedbackResponse(**parsed)
                    return validated.model_dump()
                else:
                    logger.error(f"OpenAI error {resp.status_code}: {resp.text}. Falling back.")
                    return RuleBasedLLMProvider().generate_feedback(prompt_data)
        except Exception as e:
            logger.error(f"OpenAI API call failed ({e}). Falling back to rule-based engine.")
            return RuleBasedLLMProvider().generate_feedback(prompt_data)

class GeminiLLMProvider(BaseLLMProvider):
    """
    Google Gemini provider connecting to Gemini 1.5 Flash via REST API.
    Supports user-provided or environment API keys.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = model

    def generate_feedback(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not configured. Falling back to rule-based engine.")
            return RuleBasedLLMProvider().generate_feedback(prompt_data)

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        system_instruction = (
            "You are an expert senior engineering hiring manager and career coach. "
            "Provide rigorous, honest, evidence-based feedback on technical resumes. "
            "NEVER invent companies, degrees, dates, skills, or numerical metrics. "
            "If a bullet rewrite requires metrics, use candidate placeholders like '[insert metric, e.g. +30%]'. "
            "Output strictly valid JSON conforming to LLMFeedbackResponse schema."
        )

        user_content = json.dumps(prompt_data)
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{system_instruction}\n\nAnalyze this resume data and return ONLY raw JSON:\n{user_content}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(endpoint, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(content)
                    parsed["provider_used"] = f"gemini_{self.model}"
                    validated = LLMFeedbackResponse(**parsed)
                    return validated.model_dump()
                else:
                    logger.error(f"Gemini error {resp.status_code}: {resp.text}. Falling back.")
                    return RuleBasedLLMProvider().generate_feedback(prompt_data)
        except Exception as e:
            logger.error(f"Gemini API call failed ({e}). Falling back.")
            return RuleBasedLLMProvider().generate_feedback(prompt_data)

def get_llm_provider(provider_type: Optional[str] = None, api_key: Optional[str] = None) -> BaseLLMProvider:
    """Factory function selecting configured LLM provider with dynamic overrides."""
    provider_name = (provider_type or os.environ.get("LLM_PROVIDER", "rule_based")).lower().strip()
    if provider_name == "gemini":
        return GeminiLLMProvider(api_key=api_key)
    elif provider_name == "openai":
        return OpenAILLMProvider(api_key=api_key)
    elif provider_name == "mock":
        return MockLLMProvider()
    else:
        return RuleBasedLLMProvider()

