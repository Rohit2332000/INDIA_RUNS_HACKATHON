"""
jd_embedding.py

Creates a recruiter-style semantic document from the parsed
Job Description and generates its embedding.
"""

from embeddings.embedding_model import EmbeddingModel
from jd.jd_parser import JDParser


class JDEmbeddingBuilder:

    @staticmethod
    def build_document(jd):

        document = f"""
================ ROLE ================

Experience Required:
{jd["minimum_experience"]} - {jd["maximum_experience"]} years

================ REQUIRED SKILLS ================

{", ".join(jd["skills"])}

================ EDUCATION ================

{", ".join(jd["degrees"])}

================ LOCATION ================

Preferred Locations:
{", ".join(jd["preferred_locations"])}

Work Mode:
{jd["work_mode"]}

Relocation:
{jd["relocation"]}

================ JOB DESCRIPTION ================

{jd["raw_text"]}
"""

        return document.strip()

    @classmethod
    def get_embedding(cls):

        jd = JDParser.parse()

        document = cls.build_document(jd)

        embedding = EmbeddingModel.encode(
            [document],
            normalize=True,
        )[0]

        return {

            "parsed_jd": jd,

            "document": document,

            "embedding": embedding

        }


if __name__ == "__main__":

    result = JDEmbeddingBuilder.get_embedding()

    print(result["document"])

    print("\nEmbedding Shape:", result["embedding"].shape)