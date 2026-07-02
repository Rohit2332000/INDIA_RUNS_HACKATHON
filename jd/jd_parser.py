"""
jd_parser.py

Production Job Description Parser for RecruitRankAI
"""

import re

from config.config import JOB_DESCRIPTION_FILE


class JDParser:

    # -----------------------------
    # AI / ML / Search Skills
    # -----------------------------

    SKILLS = [

        # Programming
        "python",
        "java",
        "c++",

        # Databases
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",

        # Cloud
        "aws",
        "azure",
        "gcp",

        # Containers
        "docker",
        "kubernetes",

        # Data
        "spark",
        "airflow",
        "hadoop",

        # ML
        "machine learning",
        "deep learning",
        "computer vision",
        "nlp",
        "speech recognition",
        "recommendation system",
        "ranking",
        "retrieval",
        "embeddings",

        # LLM
        "llm",
        "rag",
        "langchain",
        "langgraph",
        "transformers",
        "huggingface",

        # Fine tuning
        "lora",
        "qlora",
        "peft",
        "fine tuning",
        "fine-tuning",

        # Vector DB
        "faiss",
        "pinecone",
        "milvus",
        "weaviate",
        "qdrant",

        # Search
        "opensearch",
        "elasticsearch",
        "hybrid search",

        # Evaluation
        "ndcg",
        "mrr",
        "map",
        "a/b testing",
        "offline evaluation",

        # Models
        "bert",
        "xgboost",

        # Frameworks
        "fastapi",
        "flask",

        # Embedding Models
        "sentence-transformers",
        "bge",
        "e5",

        # Misc
        "agent",
        "agents",
        "prompt engineering"
    ]

    DEGREE_PATTERNS = {
        "phd": r"\b(ph\.?d|doctorate)\b",
        "master": r"\b(master|m\.?tech|mtech|ms|m\.s)\b",
        "bachelor": r"\b(bachelor|b\.?tech|btech|b\.?e)\b"
    }

    EXPERIENCE_PATTERN = re.compile(
        r"(\d+)\s*[-–to]+\s*(\d+)\s*years",
        re.IGNORECASE,
    )

    @staticmethod
    def load():

        with open(JOB_DESCRIPTION_FILE, encoding="utf8") as f:
            return f.read()

    @classmethod
    def parse(cls):

        text = cls.load()

        lower = text.lower()

        # -------------------------
        # Experience
        # -------------------------

        min_exp = 0
        max_exp = 0

        match = cls.EXPERIENCE_PATTERN.search(lower)

        if match:
            min_exp = int(match.group(1))
            max_exp = int(match.group(2))

        # -------------------------
        # Degrees
        # -------------------------

        degrees = []

        for degree, pattern in cls.DEGREE_PATTERNS.items():

            if re.search(pattern, lower):
                degrees.append(degree)

        # -------------------------
        # Skills
        # -------------------------

        skills = []

        for skill in cls.SKILLS:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, lower):
                skills.append(skill)

        # -------------------------
        # Work Mode
        # -------------------------

        work_mode = None

        if "hybrid" in lower:
            work_mode = "hybrid"

        elif "remote" in lower:
            work_mode = "remote"

        elif "onsite" in lower:
            work_mode = "onsite"

        # -------------------------
        # Open to Relocation
        # -------------------------

        relocation = (
            "relocation" in lower
            or "relocate" in lower
        )

        # -------------------------
        # Preferred Locations
        # -------------------------

        locations = []

        cities = [
            "noida",
            "pune",
            "hyderabad",
            "bangalore",
            "bengaluru",
            "mumbai",
            "delhi",
            "gurgaon",
            "gurugram"
        ]

        for city in cities:

            if city in lower:
                locations.append(city)

        return {

            "raw_text": text,

            "minimum_experience": min_exp,

            "maximum_experience": max_exp,

            "degrees": sorted(set(degrees)),

            "skills": sorted(set(skills)),

            "skill_count": len(set(skills)),

            "work_mode": work_mode,

            "relocation": relocation,

            "preferred_locations": sorted(set(locations)),

            "skills_text": " ".join(sorted(set(skills)))
        }