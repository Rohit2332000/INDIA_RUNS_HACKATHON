"""
skill_normalizer.py

Normalize technical skills into canonical names.

Examples
--------
ML -> machine learning
PyTorch -> pytorch
AWS -> aws
Postgres -> postgresql
"""

from typing import List

from preprocessing.text_cleaner import TextCleaner


class SkillNormalizer:

    SKILL_MAP = {

        # AI / ML
        "ml": "machine learning",
        "machine-learning": "machine learning",
        "machine learning": "machine learning",

        "ai": "artificial intelligence",
        "artificial-intelligence": "artificial intelligence",

        "nlp": "natural language processing",

        "llm": "large language models",
        "llms": "large language models",

        "rag": "retrieval augmented generation",

        "gen ai": "generative ai",
        "genai": "generative ai",

        # Programming
        "py": "python",
        "python3": "python",

        "js": "javascript",
        "ts": "typescript",

        # Databases
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "mysql": "mysql",
        "sqlite": "sqlite",

        # Cloud
        "amazon web services": "aws",
        "aws cloud": "aws",

        "gcp": "google cloud",
        "google cloud platform": "google cloud",

        "azure cloud": "azure",

        # Frameworks
        "tf": "tensorflow",

        "torch": "pytorch",

        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",

        # Data
        "spark sql": "apache spark",
        "spark": "apache spark",

        # NLP
        "lang chain": "langchain",
        "lang-chain": "langchain",

        "lang graph": "langgraph",

        # Vector DB
        "pine cone": "pinecone",

        # DevOps
        "k8s": "kubernetes",

        "docker container": "docker",
    }

    @classmethod
    def normalize_skill(cls, skill: str) -> str:

        skill = TextCleaner.clean_text(skill)

        if skill in cls.SKILL_MAP:
            return cls.SKILL_MAP[skill]

        return skill

    @classmethod
    def normalize_skills(cls, skills: List[str]) -> List[str]:

        normalized = []

        for skill in skills:

            skill = cls.normalize_skill(skill)

            if skill:
                normalized.append(skill)

        # remove duplicates while preserving order
        return list(dict.fromkeys(normalized))