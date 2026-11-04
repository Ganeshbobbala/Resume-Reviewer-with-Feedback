import re
from typing import List, Dict, Any, Set, Tuple, Optional

# Canonical Skill Taxonomy with aliases, categories, and boundary regexes
SKILL_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "JavaScript": {
        "category": "Frontend & Web",
        "aliases": ["javascript", "js", "es6", "es2020", "vanilla js"],
        "regex": r'\b(?:javascript|es6|es20\d\d)\b|\bjs\b(?!on)'
    },
    "TypeScript": {
        "category": "Frontend & Web",
        "aliases": ["typescript", "ts"],
        "regex": r'\btypescript\b|\bts\b'
    },
    "React": {
        "category": "Frontend & Web",
        "aliases": ["react", "react.js", "reactjs"],
        "regex": r'\breact(?:\.js|js)?\b'
    },
    "Next.js": {
        "category": "Frontend & Web",
        "aliases": ["next.js", "nextjs", "next"],
        "regex": r'\bnext(?:\.js|js)?\b'
    },
    "Vue.js": {
        "category": "Frontend & Web",
        "aliases": ["vue", "vue.js", "vuejs"],
        "regex": r'\bvue(?:\.js|js)?\b'
    },
    "Angular": {
        "category": "Frontend & Web",
        "aliases": ["angular", "angularjs"],
        "regex": r'\bangular(?:\.js|js)?\b'
    },
    "HTML": {
        "category": "Frontend & Web",
        "aliases": ["html", "html5"],
        "regex": r'\bhtml5?\b'
    },
    "CSS": {
        "category": "Frontend & Web",
        "aliases": ["css", "css3", "sass", "scss", "less"],
        "regex": r'\bcss3?\b|\bsass\b|\bscss\b'
    },
    "Tailwind CSS": {
        "category": "Frontend & Web",
        "aliases": ["tailwind", "tailwindcss"],
        "regex": r'\btailwind(?:\s*css)?\b'
    },
    "Redux": {
        "category": "Frontend & Web",
        "aliases": ["redux", "redux toolkit"],
        "regex": r'\bredux(?:\s*toolkit)?\b'
    },
    "Python": {
        "category": "Backend & Systems",
        "aliases": ["python", "python3"],
        "regex": r'\bpython3?\b'
    },
    "FastAPI": {
        "category": "Backend & Systems",
        "aliases": ["fastapi"],
        "regex": r'\bfastapi\b'
    },
    "Django": {
        "category": "Backend & Systems",
        "aliases": ["django"],
        "regex": r'\bdjango\b'
    },
    "Flask": {
        "category": "Backend & Systems",
        "aliases": ["flask"],
        "regex": r'\bflask\b'
    },
    "Node.js": {
        "category": "Backend & Systems",
        "aliases": ["node.js", "nodejs", "node"],
        "regex": r'\bnode(?:\.js|js)?\b'
    },
    "Express": {
        "category": "Backend & Systems",
        "aliases": ["express", "express.js"],
        "regex": r'\bexpress(?:\.js)?\b'
    },
    "Java": {
        "category": "Backend & Systems",
        "aliases": ["java", "java 8", "java 11", "java 17", "java 21"],
        "regex": r'\bjava(?:\s*\d{1,2})?\b(?!script)'
    },
    "Spring Boot": {
        "category": "Backend & Systems",
        "aliases": ["spring boot", "spring"],
        "regex": r'\bspring\s*boot\b|\bspring\s*framework\b|\bspring\b'
    },
    "Hibernate": {
        "category": "Backend & Systems",
        "aliases": ["hibernate", "jpa"],
        "regex": r'\bhibernate\b|\bjpa\b'
    },
    "Go": {
        "category": "Backend & Systems",
        "aliases": ["golang", "go programming"],
        "regex": r'\bgolang\b|\bgo\s+(?:language|programming|code|backend)\b'
    },
    "PostgreSQL": {
        "category": "Databases & Storage",
        "aliases": ["postgresql", "postgres", "pgsql"],
        "regex": r'\b(?:postgresql|postgres|pgsql)\b'
    },
    "MySQL": {
        "category": "Databases & Storage",
        "aliases": ["mysql"],
        "regex": r'\bmysql\b'
    },
    "SQL": {
        "category": "Databases & Storage",
        "aliases": ["sql", "rdbms"],
        "regex": r'\bsql\b|\brdbms\b'
    },
    "MongoDB": {
        "category": "Databases & Storage",
        "aliases": ["mongodb", "mongo"],
        "regex": r'\bmongodb\b|\bmongo\b'
    },
    "Redis": {
        "category": "Databases & Storage",
        "aliases": ["redis"],
        "regex": r'\bredis\b'
    },
    "REST API": {
        "category": "APIs & Networking",
        "aliases": ["rest", "restful", "rest api"],
        "regex": r'\brest(?:ful)?\s*(?:api|apis|services)?\b'
    },
    "GraphQL": {
        "category": "APIs & Networking",
        "aliases": ["graphql"],
        "regex": r'\bgraphql\b'
    },
    "Docker": {
        "category": "Cloud & DevOps",
        "aliases": ["docker", "containerization"],
        "regex": r'\bdocker\b|\bcontainers?\b'
    },
    "Kubernetes": {
        "category": "Cloud & DevOps",
        "aliases": ["kubernetes", "k8s"],
        "regex": r'\bkubernetes\b|\bk8s\b'
    },
    "AWS": {
        "category": "Cloud & DevOps",
        "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda"],
        "regex": r'\baws\b|\bamazon\s*web\s*services\b|\bec2\b|\bs3\b|\blambda\b'
    },
    "CI/CD": {
        "category": "Cloud & DevOps",
        "aliases": ["ci/cd", "continuous integration", "github actions", "gitlab ci", "jenkins"],
        "regex": r'\bci\s*\/\s*cd\b|\bgithub\s*actions\b|\bjenkins\b|\bgitlab\s*ci\b'
    },
    "Linux": {
        "category": "Cloud & DevOps",
        "aliases": ["linux", "ubuntu", "bash"],
        "regex": r'\blinux\b|\bubuntu\b|\bbash\b'
    },
    "Git": {
        "category": "Tools & Workflow",
        "aliases": ["git", "github", "gitlab"],
        "regex": r'\bgit\b|\bgithub\b|\bgitlab\b'
    },
    "Pandas": {
        "category": "Data Science & AI",
        "aliases": ["pandas"],
        "regex": r'\bpandas\b'
    },
    "NumPy": {
        "category": "Data Science & AI",
        "aliases": ["numpy"],
        "regex": r'\bnumpy\b'
    },
    "Scikit-learn": {
        "category": "Data Science & AI",
        "aliases": ["scikit-learn", "sklearn"],
        "regex": r'\bscikit[\s\-_]*learn\b|\bsklearn\b'
    },
    "PyTorch": {
        "category": "Data Science & AI",
        "aliases": ["pytorch"],
        "regex": r'\bpytorch\b'
    },
    "TensorFlow": {
        "category": "Data Science & AI",
        "aliases": ["tensorflow", "tf"],
        "regex": r'\btensorflow\b|\btf\b'
    },
    "Machine Learning": {
        "category": "Data Science & AI",
        "aliases": ["machine learning", "ml"],
        "regex": r'\bmachine\s*learning\b|\bml\b'
    },
    "Deep Learning": {
        "category": "Data Science & AI",
        "aliases": ["deep learning", "dl"],
        "regex": r'\bdeep\s*learning\b|\bdl\b'
    },
    "Statistics": {
        "category": "Data Science & AI",
        "aliases": ["statistics", "statistical analysis"],
        "regex": r'\bstatistics\b|\bstatistical\b'
    },
    "Spark": {
        "category": "Data Science & AI",
        "aliases": ["spark", "pyspark", "apache spark"],
        "regex": r'\b(?:apache\s*)?spark\b|\bpyspark\b'
    },
    "Figma": {
        "category": "Design & UI/UX",
        "aliases": ["figma"],
        "regex": r'\bfigma\b'
    },
    "UI/UX": {
        "category": "Design & UI/UX",
        "aliases": ["ui/ux", "user interface", "user experience"],
        "regex": r'\bui\s*\/\s*ux\b|\buser\s*experience\b|\buser\s*interface\b'
    },
    "Agile": {
        "category": "Product & Process",
        "aliases": ["agile", "scrum", "jira"],
        "regex": r'\bagile\b|\bscrum\b|\bjira\b'
    }
}

DEMONSTRATION_VERBS = re.compile(
    r'\b(developed|built|engineered|architected|designed|implemented|optimized|scaled|launched|deployed|spearheaded|migrated|refactored|automated|created|delivered)\b',
    re.IGNORECASE
)

METRIC_PATTERN = re.compile(
    r'\b(?:\d+%\s*|\$\d+[\d,]*|\d+\+?\s*(?:k|m|million|users|requests|qps|endpoints|ms|seconds))\b',
    re.IGNORECASE
)

def extract_skills_detailed(raw_text: str) -> List[Dict[str, Any]]:
    """
    Extracts skills with canonical name, alias resolution, contextual evidence,
    and classifies whether each skill is explicitly demonstrated with action
    verbs/metrics or merely mentioned in a list.
    """
    if not raw_text:
        return []

    lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
    detected_skills = {}

    current_section = "General"
    section_markers = {
        "skills": "Technical Skills",
        "experience": "Experience",
        "work": "Experience",
        "project": "Projects",
        "education": "Education",
        "summary": "Summary"
    }

    for line in lines:
        lower_line = line.lower()
        if len(line) < 40:
            for marker, sec in section_markers.items():
                if marker in lower_line:
                    current_section = sec
                    break

        for canon_name, data in SKILL_TAXONOMY.items():
            pattern = data["regex"]
            if re.search(pattern, lower_line, re.IGNORECASE):
                has_verb = bool(DEMONSTRATION_VERBS.search(line))
                has_metric = bool(METRIC_PATTERN.search(line))
                status = "demonstrated" if (has_verb or has_metric) and current_section in ["Experience", "Projects"] else "mentioned"

                if canon_name not in detected_skills or (status == "demonstrated" and detected_skills[canon_name]["status"] == "mentioned"):
                    detected_skills[canon_name] = {
                        "canonical_name": canon_name,
                        "category": data["category"],
                        "status": status,
                        "section": current_section,
                        "evidence_snippet": line[:160]
                    }

    return sorted(list(detected_skills.values()), key=lambda x: x["canonical_name"])

def extract_canonical_skills(raw_text: str) -> List[str]:
    """
    Returns sorted unique list of canonical skill names (100% backward compatible).
    """
    detailed = extract_skills_detailed(raw_text)
    return [d["canonical_name"] for d in detailed]

