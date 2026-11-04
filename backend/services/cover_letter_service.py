import re
import logging
from typing import Dict, Any, Optional

from services.skill_extractor import extract_skills

logger = logging.getLogger("cover_letter_service")

def generate_tailored_cover_letter(
    resume_text: str,
    job_description: str,
    candidate_name: Optional[str] = None,
    company_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates a professional, job-targeted cover letter based on candidate skills,
    experience points, and job description requirements.
    Follows top university career service rubrics: Hook -> Alignment -> Impact -> Close.
    """
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = [s for s in resume_skills if s in job_skills]
    if not matched_skills:
        matched_skills = resume_skills[:4]

    target_company = company_name or "your team"
    target_role = "the open position"

    # Infer potential role title from job description
    role_match = re.search(r'(?:role|position|seeking a|hiring a|looking for an?)\s+([A-Za-z\s]{3,30})(?:developer|engineer|specialist|architect|analyst|manager)', job_description, re.IGNORECASE)
    if role_match:
        target_role = role_match.group(0).strip()
    else:
        # Fallback to simple matching
        for title in ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Scientist", "DevOps Engineer", "Software Engineer"]:
            if title.lower() in job_description.lower():
                target_role = title
                break

    name = candidate_name or "Applicant"
    top_skills_str = ", ".join(matched_skills[:3]) if matched_skills else "modern software engineering tools"

    # Letter Paragraphs
    paragraph_1 = (
        f"Dear Hiring Team,\n\n"
        f"I am writing to express my enthusiastic interest in {target_role} at {target_company}. "
        f"With hands-on experience in {top_skills_str} and a focus on delivering high-performance, user-centric software, "
        f"I am excited by the opportunity to contribute directly to {target_company}'s engineering objectives."
    )

    paragraph_2 = (
        f"Throughout my technical experience, I have specialized in building robust, maintainable systems using {', '.join(matched_skills[:4])}. "
        f"My background emphasizes writing clean code, collaborating across cross-functional teams, and optimizing application responsiveness. "
        f"I approach engineering challenges by identifying core bottlenecks and implementing scalable solutions that measurably improve operational outcomes."
    )

    paragraph_3 = (
        f"What excites me most about {target_company} is your focus on technical excellence and real-world impact. "
        f"Given my proficiency with {matched_skills[0] if matched_skills else 'core system design'} and enthusiasm for continuous learning, "
        f"I am confident I can quickly onboard and bring immediate momentum to your upcoming roadmaps."
    )

    paragraph_4 = (
        f"Thank you for your time and consideration. I would welcome the opportunity to discuss how my technical qualifications "
        f"and problem-solving mindset align with your needs for this role.\n\n"
        f"Sincerely,\n{name}"
    )

    full_letter = f"{paragraph_1}\n\n{paragraph_2}\n\n{paragraph_3}\n\n{paragraph_4}"

    return {
        "cover_letter": full_letter,
        "target_role": target_role,
        "matched_skills_highlighted": matched_skills[:5],
        "word_count": len(full_letter.split())
    }

