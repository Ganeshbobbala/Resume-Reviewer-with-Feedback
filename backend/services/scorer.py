import re
from typing import List, Dict, Any

ROLE_SKILLS: Dict[str, List[str]] = {
    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "typescript",
        "git"
    ],

    "Backend Developer": [
        "python",
        "node.js",
        "express",
        "sql",
        "mongodb",
        "rest api",
        "git"
    ],

    "Full Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "express",
        "sql",
        "git"
    ],

    "Java Developer": [
        "java",
        "spring",
        "spring boot",
        "sql",
        "jdbc",
        "hibernate",
        "git"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "scikit-learn",
        "machine learning",
        "statistics",
        "sql"
    ],

    "ML Engineer": [
        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "numpy",
        "pandas"
    ],

    "Data Engineer": [
        "python",
        "sql",
        "pandas",
        "spark",
        "hadoop",
        "cloud",
        "git"
    ],

    "DevOps Engineer": [
        "docker",
        "kubernetes",
        "aws",
        "ci/cd",
        "linux",
        "python",
        "git"
    ],

    "Cloud Architect": [
        "aws",
        "cloud",
        "docker",
        "kubernetes",
        "microservices",
        "networking",
        "git"
    ],

    "Android Developer": [
        "kotlin",
        "java",
        "android",
        "rest api",
        "git"
    ],

    "iOS Developer": [
        "swift",
        "ios",
        "rest api",
        "git"
    ],

    "Cybersecurity Analyst": [
        "cybersecurity",
        "networking",
        "linux",
        "python",
        "sql"
    ],

    "QA / Automation Engineer": [
        "selenium",
        "testing",
        "python",
        "javascript",
        "git"
    ],

    "UI/UX Designer": [
        "figma",
        "ui/ux",
        "prototyping",
        "html",
        "css"
    ],

    "Product Manager": [
        "agile",
        "scrum",
        "jira",
        "product management",
        "data analysis"
    ]
}

# Display names for canonical formatting
CANONICAL_ROLE_SKILL_NAMES = {
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript",
    "react": "React",
    "typescript": "TypeScript",
    "git": "Git",
    "python": "Python",
    "node.js": "Node.js",
    "express": "Express",
    "sql": "SQL",
    "mongodb": "MongoDB",
    "rest api": "REST API",
    "java": "Java",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    "jdbc": "JDBC",
    "hibernate": "Hibernate",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn",
    "machine learning": "Machine Learning",
    "statistics": "Statistics",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "cloud": "Cloud (AWS/GCP/Azure)",
    "ci/cd": "CI/CD",
    "linux": "Linux",
    "spark": "Apache Spark",
    "hadoop": "Hadoop",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "android": "Android SDK",
    "ios": "iOS / Xcode",
    "cybersecurity": "Cybersecurity",
    "networking": "Networking",
    "selenium": "Selenium",
    "testing": "Software Testing / QA",
    "figma": "Figma",
    "ui/ux": "UI/UX Design",
    "prototyping": "Prototyping",
    "agile": "Agile Methodology",
    "scrum": "Scrum Framework",
    "jira": "Jira",
    "product management": "Product Management",
    "data analysis": "Data Analysis",
    "microservices": "Microservices"
}

SECTION_PATTERNS = {
    "contact": [
        r'\bcontact\b', r'\bemail\b', r'\bphone\b', r'\blinkedin\b', r'\bgithub\b', r'\baddress\b', r'\b\S+@\S+\.\S+\b'
    ],
    "summary": [
        r'\b(?:professional\s+)?summary\b', r'\bprofile\b', r'\bobjective\b', r'\babout\s+me\b', r'\boverview\b'
    ],
    "education": [
        r'\beducation\b', r'\bacademics?\b', r'\bdegree\b', r'\buniversity\b', r'\bcollege\b', r'\bbachelor\b', r'\bmaster\b', r'\bb\.?tech\b', r'\bm\.?tech\b', r'\bb\.?s\.?\b'
    ],
    "skills": [
        r'\bskills?\b', r'\btechnical\s+skills?\b', r'\btechnologies\b', r'\bcompetencies\b', r'\bexpertise\b'
    ],
    "projects": [
        r'\bprojects?\b', r'\bpersonal\s+projects?\b', r'\bkey\s+projects?\b', r'\bacademics?\s+projects?\b'
    ],
    "experience": [
        r'\b(?:work\s+)?experience\b', r'\bemployment\b', r'\bwork\s+history\b', r'\binternships?\b', r'\bcareer\b'
    ],
    "certifications": [
        r'\bcertifications?\b', r'\bcertificates?\b', r'\blicenses?\b', r'\bcertified\b'
    ],
    "achievements": [
        r'\bachievements?\b', r'\bawards?\b', r'\bhonors?\b', r'\baccomplishments?\b'
    ]
}

def analyze_resume_sections(raw_text: str) -> Dict[str, bool]:
    """
    Detects presence of key resume sections in the text.
    """
    text_lower = raw_text.lower()
    sections = {}
    for section_key, patterns in SECTION_PATTERNS.items():
        found = any(re.search(pattern, text_lower) for pattern in patterns)
        sections[section_key] = found
    return sections

def calculate_scores(detected_skills: List[str], raw_text: str, target_role: str) -> Dict[str, Any]:
    """
    Computes explainable scores:
      - Skill Score (40%)
      - Section Score (30%)
      - Job Match Score (20%)
      - Keyword Score (10%)
    Calculates final_score = (skill_score * 0.40) + (section_score * 0.30) + (job_match_score * 0.20) + (keyword_score * 0.10)
    """
    # Normalize detected skills to lower case set for lookup
    detected_set = {s.lower() for s in detected_skills}
    
    # Get target role required skills
    role_skills_lower = ROLE_SKILLS.get(target_role, ROLE_SKILLS["Frontend Developer"])
    
    matched_skills = []
    missing_skills = []
    
    for s_lower in role_skills_lower:
        canonical_name = CANONICAL_ROLE_SKILL_NAMES.get(s_lower, s_lower.title())
        # Check direct or partial match
        if s_lower in detected_set or any(s_lower in d for d in detected_set):
            matched_skills.append(canonical_name)
        else:
            missing_skills.append(canonical_name)
            
    # Job match percentage
    total_req = len(role_skills_lower)
    job_match_score = round((len(matched_skills) / total_req) * 100) if total_req > 0 else 50

    # Skill score (based on ratio of matched skills + total richness of skills detected)
    base_skill_ratio = len(matched_skills) / total_req if total_req > 0 else 0.5
    extra_skills_bonus = min(0.2, len(detected_skills) * 0.02)
    skill_score = min(100, round((base_skill_ratio * 0.8 + extra_skills_bonus) * 100))
    
    # Section score
    sections = analyze_resume_sections(raw_text)
    # Give higher weight to critical sections (contact, education, skills, experience, projects)
    core_sections = ["contact", "education", "skills", "experience", "projects"]
    optional_sections = ["summary", "certifications", "achievements"]
    
    core_count = sum(1 for sec in core_sections if sections.get(sec))
    opt_count = sum(1 for sec in optional_sections if sections.get(sec))
    
    section_score = round(((core_count / len(core_sections)) * 80) + ((opt_count / len(optional_sections)) * 20))

    # Keyword score (keyword density & presence of action verbs, impact numbers, tools)
    text_lower = raw_text.lower()
    keyword_matches = sum(1 for kw in role_skills_lower if kw in text_lower)
    has_numbers = bool(re.search(r'\b\d+(?:%|\+|\s*k|\s*m)?\b', text_lower))
    has_action_verbs = bool(re.search(r'\b(developed|built|managed|led|created|designed|implemented|optimized|increased|reduced)\b', text_lower))
    
    kw_ratio = keyword_matches / total_req if total_req > 0 else 0.5
    kw_base = kw_ratio * 70
    if has_numbers:
        kw_base += 15
    if has_action_verbs:
        kw_base += 15
    keyword_score = min(100, round(kw_base))

    # Final Score Formula (Preserved exact weights: 40% Skills, 30% Structure, 20% Job Match, 10% Keywords)
    final_score = round(
        (skill_score * 0.40) +
        (section_score * 0.30) +
        (job_match_score * 0.20) +
        (keyword_score * 0.10)
    )

    # Detailed Skill Demonstration Attribution
    from services.skill_taxonomy import extract_skills_detailed
    detailed_skills = extract_skills_detailed(raw_text)
    
    demonstrated_skills = [d for d in detailed_skills if d.get("status") == "demonstrated"]
    mentioned_only_skills = [d for d in detailed_skills if d.get("status") == "mentioned"]

    # Classify Target Role Requirements into Matched, Insufficiently Demonstrated, and Missing
    matched_set = {m.lower() for m in matched_skills}
    demonstrated_names = {d["canonical_name"].lower() for d in demonstrated_skills}
    
    insufficiently_demonstrated = []
    for m in matched_skills:
        if m.lower() not in demonstrated_names:
            insufficiently_demonstrated.append(m)

    # Missing evidence notes
    missing_evidence = []
    if missing_skills:
        missing_evidence.append(f"No evidence found for core {target_role} requirements: {', '.join(missing_skills[:3])}.")
    if insufficiently_demonstrated:
        missing_evidence.append(f"Listed but lacks demonstrated impact/metrics in Experience section: {', '.join(insufficiently_demonstrated[:3])}.")
    if not sections.get("projects"):
        missing_evidence.append("Projects section is missing. Portfolio projects provide vital proof of hands-on ability.")

    # Specific actionable improvement suggestions
    actionable_suggestions = []
    if not has_numbers:
        actionable_suggestions.append("Quantify accomplishments in your bullet points with metrics (e.g. latency reduced by 40%, served 50k users).")
    if not has_action_verbs:
        actionable_suggestions.append("Begin experience bullet points with strong active verbs (e.g. 'Architected', 'Engineered', 'Optimized').")
    if insufficiently_demonstrated:
        actionable_suggestions.append(f"Incorporate technical details explaining how you used {insufficiently_demonstrated[0]} in your projects.")
    if missing_skills:
        actionable_suggestions.append(f"Add projects showcasing experience in {missing_skills[0]} to close role gaps.")

    # Transparent, explainable component breakdown
    score_breakdown = {
        "overall_score": final_score,
        "disclaimer": "Diagnostic suitability score based on transparent heuristic rubrics. Not an official ATS score or guarantee of interview selection.",
        "components": {
            "skill_match": {
                "score": skill_score,
                "weight": 0.40,
                "contribution": round(skill_score * 0.40, 1),
                "explanation": f"Evaluates breadth and depth of skills matching {target_role} requirements."
            },
            "resume_structure": {
                "score": section_score,
                "weight": 0.30,
                "contribution": round(section_score * 0.30, 1),
                "explanation": f"Evaluates presence of critical sections: {core_count}/{len(core_sections)} core sections present."
            },
            "role_alignment": {
                "score": job_match_score,
                "weight": 0.20,
                "contribution": round(job_match_score * 0.20, 1),
                "explanation": f"Direct coverage percentage: {len(matched_skills)} of {total_req} required track competencies matched."
            },
            "impact_keywords": {
                "score": keyword_score,
                "weight": 0.10,
                "contribution": round(keyword_score * 0.10, 1),
                "explanation": f"Evaluates keyword density ({keyword_matches}/{total_req} terms), action verbs ({'yes' if has_action_verbs else 'no'}), and metrics ({'yes' if has_numbers else 'no'})."
            }
        },
        "demonstrated_skills_count": len(demonstrated_skills),
        "mentioned_only_count": len(mentioned_only_skills),
        "missing_evidence": missing_evidence,
        "actionable_suggestions": actionable_suggestions
    }

    return {
        # Preserved baseline contract
        "resume_score": final_score,
        "skill_score": skill_score,
        "section_score": section_score,
        "job_match_score": job_match_score,
        "keyword_score": keyword_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "sections": sections,

        # New explainable scoring & skill extraction additions
        "score_breakdown": score_breakdown,
        "detailed_skills": detailed_skills[:25],
        "demonstrated_skills": [d["canonical_name"] for d in demonstrated_skills],
        "insufficiently_demonstrated_skills": insufficiently_demonstrated,
        "required_skills_count": total_req,
        "matched_skills_count": len(matched_skills)
    }
