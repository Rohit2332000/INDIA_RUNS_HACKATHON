"""
certification_parser.py

Parses candidate certifications and categorizes them.
"""

from preprocessing.text_cleaner import TextCleaner


class CertificationParser:

    AI_CERTIFICATIONS = {
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "tensorflow",
        "pytorch",
        "hugging face",
        "huggingface",
        "llm",
        "generative ai",
        "langchain",
        "langgraph",
        "rag",
        "nlp",
        "computer vision",
        "openai",
    }

    CLOUD_CERTIFICATIONS = {
        "aws",
        "amazon web services",
        "azure",
        "gcp",
        "google cloud",
        "google cloud platform",
        "kubernetes",
        "docker",
    }

    DATA_CERTIFICATIONS = {
        "sql",
        "power bi",
        "tableau",
        "snowflake",
        "spark",
        "databricks",
        "airflow",
    }

    @classmethod
    def parse(cls, candidate):

        certs = candidate.get("certifications", [])

        names = []

        ai = []
        cloud = []
        data = []

        for cert in certs:

            if isinstance(cert, dict):

                name = (
                    cert.get("name")
                    or cert.get("title")
                    or cert.get("certificate")
                    or ""
                )

            else:

                name = str(cert)

            name = TextCleaner.clean_text(name)

            if not name:
                continue

            names.append(name)

            if any(keyword in name for keyword in cls.AI_CERTIFICATIONS):
                ai.append(name)

            if any(keyword in name for keyword in cls.CLOUD_CERTIFICATIONS):
                cloud.append(name)

            if any(keyword in name for keyword in cls.DATA_CERTIFICATIONS):
                data.append(name)

        names = list(dict.fromkeys(names))
        ai = list(dict.fromkeys(ai))
        cloud = list(dict.fromkeys(cloud))
        data = list(dict.fromkeys(data))

        return {

            "certifications": names,

            "certification_count": len(names),

            "ai_certifications": ai,

            "cloud_certifications": cloud,

            "data_certifications": data,

            "ai_certification_count": len(ai),

            "cloud_certification_count": len(cloud),

            "data_certification_count": len(data),

            "certification_text": " ".join(names)

        }