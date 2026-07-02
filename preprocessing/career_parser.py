"""
career_parser.py

Extracts useful information from candidate career history.
"""

from preprocessing.text_cleaner import TextCleaner


class CareerParser:

    @staticmethod
    def parse(candidate: dict) -> dict:

        history = candidate.get("career_history", [])

        companies = []
        titles = []
        industries = []

        total_months = 0
        current_company = ""
        current_title = ""

        for job in history:

            companies.append(
                TextCleaner.clean_text(
                    job.get("company", "")
                )
            )

            titles.append(
                TextCleaner.normalize_title(
                    job.get("title", "")
                )
            )

            industries.append(
                TextCleaner.clean_text(
                    job.get("industry", "")
                )
            )

            total_months += int(
                job.get("duration_months", 0)
            )

            if job.get("is_current", False):

                current_company = TextCleaner.clean_text(
                    job.get("company", "")
                )

                current_title = TextCleaner.normalize_title(
                    job.get("title", "")
                )

        return {

    "companies": list(dict.fromkeys(companies)),

    "titles": list(dict.fromkeys(titles)),

    "industries": list(dict.fromkeys(industries)),

    "career_months": total_months,

    "career_years": round(total_months / 12, 2),

    "current_company": current_company,

    "current_title": current_title,

    "job_count": len(history),

    # New Features
    "avg_tenure_months": round(
        total_months / max(len(history), 1),
        2
    ),

    "career_stability_score": round(
        min(total_months / (12 * max(len(history), 1)), 5),
        2
    ),

    "company_count": len(set(companies)),

    "title_count": len(set(titles))

}