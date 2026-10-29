from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StrengthItem(BaseModel):
    strength: str = Field(..., description="High-level description of candidate strength")
    supporting_excerpt: str = Field(..., description="Exact or near-exact supporting excerpt from resume text")
    relevance: str = Field(..., description="Why this strength is relevant to target role")

class MissingSkillItem(BaseModel):
    skill: str = Field(..., description="Required skill name")
    status: str = Field(..., description="'missing' or 'insufficiently_demonstrated'")
    recommendation: str = Field(..., description="Actionable recommendation on how to demonstrate or acquire this skill")

class SectionSuggestion(BaseModel):
    section: str = Field(..., description="Resume section name, e.g. Experience, Projects, Skills")
    critique: str = Field(..., description="Identified area for improvement")
    recommendation: str = Field(..., description="Specific, actionable advice for revising this section")

class BulletRewrite(BaseModel):
    original_bullet: str = Field(..., description="Original bullet text from candidate resume")
    improved_bullet: str = Field(..., description="Improved rewrite using strong action verb and ACR structure")
    framework_used: str = Field("Action-Context-Result", description="Framework applied")
    metric_placeholder: Optional[str] = Field(None, description="Candidate-provided placeholder prompt for unverified numbers (e.g. '[insert metric, e.g. +30%]')")

class RAGCitation(BaseModel):
    source_title: str = Field(..., description="Source document title, e.g. Harvard OCS Guide")
    section: str = Field(..., description="Source section or rubric")
    key_principle: str = Field(..., description="Relevant principle or citation excerpt applied")

class LLMFeedbackResponse(BaseModel):
    resume_summary: str = Field(..., description="Objective 2-3 sentence technical profile summary")
    verified_strengths: List[StrengthItem] = Field(default_factory=list, description="Strengths verified with resume text proof")
    skill_gaps: List[MissingSkillItem] = Field(default_factory=list, description="Missing or insufficiently demonstrated required skills")
    job_specific_recommendations: List[str] = Field(default_factory=list, description="Tailored recommendations for target track")
    section_suggestions: List[SectionSuggestion] = Field(default_factory=list, description="Section-by-section enhancement critique")
    bullet_rewrites: List[BulletRewrite] = Field(default_factory=list, description="Before and after bullet rewrites with unverified metric placeholders")
    supporting_evidence: List[str] = Field(default_factory=list, description="Verifiable facts and projects confirmed in resume")
    rag_citations: List[RAGCitation] = Field(default_factory=list, description="Grounded career guide and screening rubric citations")
    prioritized_next_steps: List[str] = Field(default_factory=list, description="Top 3 high-impact action items ordered by priority")
    limitations_and_uncertainty: str = Field(
        "Heuristic analysis based on supplied resume text. Does not guarantee interview selection.",
        description="Explicit disclosure of automated evaluation boundaries"
    )
    provider_used: str = Field("rule_based", description="LLM provider or rule engine that generated the feedback")
