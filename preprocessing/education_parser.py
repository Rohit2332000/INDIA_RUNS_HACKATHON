"""
education_parser.py

Parses and normalizes candidate education information.
"""

import re

from preprocessing.text_cleaner import TextCleaner


class EducationParser:

    DEGREE_PRIORITY = {
        "phd": 5,
        "doctorate": 5,
        "mba": 4,
        "master": 4,
        "bachelor": 3,
        "undergraduate": 3,
        "associate": 2,
        "diploma": 1,
        "certificate": 1,
    }

    DEGREE_ALIASES = {
        # Bachelor's
        "be": "bachelor",
        "b e": "bachelor",
        "beng": "bachelor",
        "btech": "bachelor",
        "b tech": "bachelor",
        "bachelor of engineering": "bachelor",
        "bachelor of technology": "bachelor",
        "bachelor of science": "bachelor",
        "bs": "bachelor",
        "bsc": "bachelor",

        # Master's
        "me": "master",
        "m e": "master",
        "meng": "master",
        "mtech": "master",
        "m tech": "master",
        "master of engineering": "master",
        "master of technology": "master",
        "master of science": "master",
        "msc": "master",
        "ms": "master",

        # MBA
        "mba": "mba",

        # PhD
        "phd": "phd",
        "doctor of philosophy": "phd",
        "doctorate": "phd",
    }

    CS_KEYWORDS = [
        "computer science",
        "computer engineering",
        "software engineering",
        "artificial intelligence",
        "machine learning",
        "data science",
        "information technology",
        "informatics",
        "electronics",
        "electrical engineering",
    ]

    @classmethod
    def normalize_degree(cls, degree: str):

        degree = TextCleaner.clean_text(degree)

        degree = re.sub(r"[^a-z0-9 ]", "", degree)

        return cls.DEGREE_ALIASES.get(degree, degree)

    @classmethod
    def degree_score(cls, degree: str):

        degree = cls.normalize_degree(degree)

        for key, score in cls.DEGREE_PRIORITY.items():

            if key in degree:
                return score

        return 0

    @classmethod
    def parse(cls, candidate):

        education = candidate.get("education", [])

        institutions = []
        degrees = []
        fields = []

        highest_degree = ""
        highest_score = -1
        graduation_year = 0

        cs_related = False

        for edu in education:

            institution = TextCleaner.clean_text(
                edu.get("institution", "")
            )

            degree = TextCleaner.clean_text(
                edu.get("degree", "")
            )

            field = TextCleaner.clean_text(
                edu.get("field_of_study", "")
            )

            year = edu.get("end_year", 0)

            institutions.append(institution)
            degrees.append(degree)
            fields.append(field)

            score = cls.degree_score(degree)

            if score > highest_score:

                highest_score = score
                highest_degree = degree

            if year > graduation_year:
                graduation_year = year

            for keyword in cls.CS_KEYWORDS:

                if keyword in field:
                    cs_related = True
                    break

        if highest_score < 0:
            highest_score = 0

        return {

            "institutions": list(dict.fromkeys(institutions)),

            "degrees": list(dict.fromkeys(degrees)),

            "fields": list(dict.fromkeys(fields)),

            "highest_degree": highest_degree,

            "degree_score": highest_score,

            "graduation_year": graduation_year,

            "education_count": len(education),

            "cs_related_degree": cs_related,

            "education_text": " ".join(
                institutions + degrees + fields
            )

        }