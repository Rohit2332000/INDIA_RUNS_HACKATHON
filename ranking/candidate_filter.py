"""
candidate_filter.py

Pre-filter candidates before semantic retrieval.

This removes obviously irrelevant candidates while keeping
enough candidates for semantic search and hybrid ranking.
"""

import pandas as pd


class CandidateFilter:

    NEGATIVE_TITLES = {
        "hr manager",
        "graphic designer",
        "marketing manager",
        "sales manager",
        "sales executive",
        "accountant",
    }

    @classmethod
    def filter(cls, df: pd.DataFrame, jd: dict) -> pd.DataFrame:

        filtered = df.copy()

        # --------------------------------------------------
        # Experience Filter
        # Allow candidates with up to 2 years less experience
        # --------------------------------------------------

        minimum_exp = jd.get("minimum_experience", 0)

        filtered = filtered[
            filtered["career_years"] >= max(0, minimum_exp - 2)
        ]

        # --------------------------------------------------
        # Basic AI Skill Filter
        # Candidate should have at least one AI skill
        # --------------------------------------------------

        filtered = filtered[
            filtered["ai_skill_count"] >= 1
        ]

        # --------------------------------------------------
        # Remove Clearly Irrelevant Titles
        # --------------------------------------------------

        filtered = filtered[
            ~filtered["current_title"]
            .fillna("")
            .str.lower()
            .isin(cls.NEGATIVE_TITLES)
        ]

        # --------------------------------------------------
        # Reset Index
        # --------------------------------------------------

        filtered = filtered.reset_index(drop=True)

        return filtered