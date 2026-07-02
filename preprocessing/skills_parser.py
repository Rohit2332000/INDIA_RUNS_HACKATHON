"""
skills_parser.py

Production-grade skill parser for RecruitRankAI.
"""

from preprocessing.skill_normalizer import SkillNormalizer


class SkillsParser:

    CATEGORY_MAP = {

        "ai": {
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "natural language processing",
            "computer vision",
            "image classification",
            "object detection",
            "speech recognition",
            "tts",
            "asr",
            "transformers",
            "huggingface",
            "openai",
            "llama",
            "mistral",
            "gemma",
            "langchain",
            "langgraph",
            "retrieval augmented generation",
            "rag",
            "fine tuning",
            "fine-tuning",
            "fine-tuning llms",
            "llm",
            "llms",
            "large language models",
            "generative ai",
            "gans",
            "diffusion",
            "stable diffusion",
            "lora",
            "tensorflow",
            "pytorch",
            "keras",
        },

        "programming": {
            "python",
            "java",
            "javascript",
            "typescript",
            "c",
            "c++",
            "c#",
            "go",
            "rust",
            "scala",
            "r",
        },

        "database": {
            "mysql",
            "postgresql",
            "mongodb",
            "redis",
            "sqlite",
            "oracle",
            "snowflake",
        },

        "cloud": {
            "aws",
            "google cloud",
            "azure",
            "docker",
            "kubernetes",
        },

        "vector_db": {
            "faiss",
            "pinecone",
            "milvus",
            "chromadb",
            "weaviate",
            "qdrant",
        },

        "mlops": {
            "mlflow",
            "weights & biases",
            "wandb",
            "bentoml",
            "kubeflow",
            "airflow",
            "dvc",
        },

        "data_engineering": {
            "apache spark",
            "spark",
            "apache beam",
            "hadoop",
            "kafka",
            "databricks",
            "etl",
        },

        "backend": {
            "flask",
            "fastapi",
            "django",
            "spring",
            "node.js",
            "express",
        },

        "frontend": {
            "react",
            "angular",
            "vue",
            "tailwind",
            "html",
            "css",
        },

        "analytics": {
            "power bi",
            "tableau",
            "excel",
            "statistics",
            "statistical modeling",
        },
    }

    @classmethod
    def match_category(cls, skill: str):

        skill = skill.lower().strip()

        categories = []

        for category, keywords in cls.CATEGORY_MAP.items():

            if skill in keywords:
                categories.append(category)

        return categories

    @classmethod
    def parse(cls, candidate):

        raw = candidate.get("skills", [])

        skills = []

        for item in raw:

            if isinstance(item, dict):

                value = (
                    item.get("skill")
                    or item.get("name")
                    or item.get("title")
                    or ""
                )

            else:

                value = str(item)

            skills.append(value)

        skills = SkillNormalizer.normalize_skills(skills)

        category_results = {
            category: []
            for category in cls.CATEGORY_MAP
        }

        others = []

        for skill in skills:

            matched = cls.match_category(skill)

            if matched:

                for cat in matched:
                    category_results[cat].append(skill)

            else:

                others.append(skill)

        # Remove duplicates
        for key in category_results:

            category_results[key] = list(
                dict.fromkeys(category_results[key])
            )

        return {

            "skills": skills,

            "skill_count": len(skills),

            "ai_skills": category_results["ai"],
            "programming_skills": category_results["programming"],
            "database_skills": category_results["database"],
            "cloud_skills": category_results["cloud"],
            "vector_db_skills": category_results["vector_db"],
            "mlops_skills": category_results["mlops"],
            "data_engineering_skills": category_results["data_engineering"],
            "backend_skills": category_results["backend"],
            "frontend_skills": category_results["frontend"],
            "analytics_skills": category_results["analytics"],

            "other_skills": others,

            "ai_skill_count": len(category_results["ai"]),
            "programming_skill_count": len(category_results["programming"]),
            "database_skill_count": len(category_results["database"]),
            "cloud_skill_count": len(category_results["cloud"]),
            "vector_db_skill_count": len(category_results["vector_db"]),
            "mlops_skill_count": len(category_results["mlops"]),
            "data_engineering_skill_count": len(category_results["data_engineering"]),
            "backend_skill_count": len(category_results["backend"]),
            "frontend_skill_count": len(category_results["frontend"]),
            "analytics_skill_count": len(category_results["analytics"]),

            "skills_text": " ".join(skills),
        }