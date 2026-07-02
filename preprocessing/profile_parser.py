"""
profile_parser.py

Extract and normalize profile information from a candidate.
"""

from preprocessing.text_cleaner import TextCleaner


class ProfileParser:

    @staticmethod
    def parse(candidate: dict) -> dict:
        profile = candidate.get("profile", {})

        return {
            "headline": TextCleaner.clean_text(
                profile.get("headline", "")
            ),

            "summary": TextCleaner.clean_text(
                profile.get("summary", "")
            ),

            "location": TextCleaner.clean_text(
                profile.get("location", "")
            ),

            "country": TextCleaner.clean_text(
                profile.get("country", "")
            ),

            "years_experience": float(
                profile.get("years_of_experience", 0)
            ),

            "current_title": TextCleaner.normalize_title(
                profile.get("current_title", "")
            ),

            "current_company": TextCleaner.clean_text(
                profile.get("current_company", "")
            ),

            "current_company_size": TextCleaner.clean_text(
                profile.get("current_company_size", "")
            ),

            "current_industry": TextCleaner.clean_text(
                profile.get("current_industry", "")
            )
        }