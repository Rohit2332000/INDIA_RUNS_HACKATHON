"""
feature_builder.py

Creates engineered features for hybrid ranking.
"""

import pandas as pd


class FeatureBuilder:

    @staticmethod
    def technical_score(row):

        score = (
            row["ai_skill_count"] * 5
            + row["programming_skill_count"] * 3
            + row["cloud_skill_count"] * 2
            + row["database_skill_count"] * 2
            + row["backend_skill_count"] * 1
            + row["mlops_skill_count"] * 2
            + row["vector_db_skill_count"] * 2
        )

        return round(score, 2)

    @staticmethod
    def education_score(row):

        score = row["degree_score"]

        if row["cs_related_degree"]:
            score += 2

        return score

    @staticmethod
    def experience_score(row):

        years = row["career_years"]

        if years >= 10:
            return 10

        return round(years, 2)

    @staticmethod
    def career_score(row):

        return round(
            row["career_stability_score"] * 2,
            2,
        )

    @staticmethod
    def certification_score(row):

        return (
            row["ai_certification_count"] * 3
            + row["cloud_certification_count"] * 2
            + row["data_certification_count"] * 2
        )

    @staticmethod
    def candidate_quality_score(row):

        score = (
            row["technical_score"] * 0.40
            + row["experience_score"] * 0.20
            + row["behavior_score"] * 10 * 0.20
            + row["education_score"] * 0.10
            + row["certification_score"] * 0.10
        )

        return round(score, 2)

    @classmethod
    def build(cls, df):

        df = df.copy()

        df["technical_score"] = df.apply(
            cls.technical_score,
            axis=1,
        )

        df["education_score"] = df.apply(
            cls.education_score,
            axis=1,
        )

        df["experience_score"] = df.apply(
            cls.experience_score,
            axis=1,
        )

        df["career_score"] = df.apply(
            cls.career_score,
            axis=1,
        )

        df["certification_score"] = df.apply(
            cls.certification_score,
            axis=1,
        )

        df["candidate_quality_score"] = df.apply(
            cls.candidate_quality_score,
            axis=1,
        )

        return df