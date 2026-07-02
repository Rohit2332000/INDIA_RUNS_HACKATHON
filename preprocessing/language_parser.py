"""
language_parser.py

Parses candidate languages and proficiency levels.
"""

from preprocessing.text_cleaner import TextCleaner


class LanguageParser:

    PROFICIENCY_LEVELS = {
        "native": 4,
        "fluent": 3,
        "professional": 3,
        "advanced": 3,
        "intermediate": 2,
        "conversational": 2,
        "basic": 1,
        "beginner": 1,
    }

    @classmethod
    def parse(cls, candidate):

        languages = candidate.get("languages", [])

        language_names = []

        professional_languages = []

        native_languages = []

        proficiency_scores = []

        for lang in languages:

            if not isinstance(lang, dict):
                continue

            name = TextCleaner.clean_text(
                lang.get("language", "")
            )

            proficiency = TextCleaner.clean_text(
                lang.get("proficiency", "")
            )

            if not name:
                continue

            language_names.append(name)

            score = cls.PROFICIENCY_LEVELS.get(proficiency, 0)

            proficiency_scores.append(score)

            if proficiency in [
                "professional",
                "advanced",
                "fluent",
            ]:
                professional_languages.append(name)

            if proficiency == "native":
                native_languages.append(name)

        avg_score = (
            round(sum(proficiency_scores) / len(proficiency_scores), 2)
            if proficiency_scores
            else 0
        )

        return {

            "languages": language_names,

            "language_count": len(language_names),

            "professional_languages": professional_languages,

            "native_languages": native_languages,

            "professional_language_count": len(professional_languages),

            "native_language_count": len(native_languages),

            "average_language_score": avg_score,

            "languages_text": " ".join(language_names)

        }