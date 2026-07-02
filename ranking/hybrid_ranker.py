"""
hybrid_ranker.py

Hybrid Recruiter Ranking Engine

Combines:

1. Semantic Similarity
2. Skill Match
3. Experience Fit
4. Title Match
5. Technical Strength
6. Education
7. Behaviour
8. Career Stability
9. Location Fit

Outputs the final ranked candidates.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from embeddings.semantic_search import SemanticSearch
from jd.jd_parser import JDParser


class HybridRanker:

    """
    Production Hybrid Candidate Ranker
    """

    # ----------------------------------------------------
    # Weights
    # ----------------------------------------------------
    WEIGHTS = {

    "semantic": 0.60,

    "skills": 0.20,

    "experience": 0.08,

    "title": 0.05,

    "technical": 0.04,

    "education": 0.01,

    "behavior": 0.01,

    "career": 0.00,

    "location": 0.01,
    }

    # ----------------------------------------------------
    # Preferred AI Titles
    # ----------------------------------------------------

    AI_TITLES = {

        "ai engineer",

        "ml engineer",

        "machine learning engineer",

        "deep learning engineer",

        "nlp engineer",

        "computer vision engineer",

        "data scientist",

        "applied scientist",

        "research engineer",

        "recommendation systems engineer",

        "search engineer",

        "llm engineer",

        "genai engineer",

        "backend engineer",
    }

    # ----------------------------------------------------

    def __init__(self):

        self.jd = JDParser.parse()

        self.search = SemanticSearch()

        self.df = self.search.search()

    # ----------------------------------------------------
    # Utilities
    # ----------------------------------------------------

    @staticmethod
    def normalize(series):

        minimum = series.min()

        maximum = series.max()

        if maximum == minimum:

            return np.ones(len(series))

        return (series - minimum) / (maximum - minimum)

    # ----------------------------------------------------

    @staticmethod
    def safe_set(values):

        if values is None:

            return set()

        if isinstance(values, list):

            return {str(v).lower() for v in values}

        if isinstance(values, str):

            return {values.lower()}

        return set()

    # ----------------------------------------------------
    # Add normalized numeric features
    # ----------------------------------------------------

    def normalize_features(self):

        df = self.df

        df["technical_norm"] = self.normalize(
            df["ai_skill_count"]
            + df["cloud_skill_count"]
            + df["vector_db_skill_count"]
            + df["mlops_skill_count"]
            + df["backend_skill_count"]
            + df["data_engineering_skill_count"]
        )

        df["experience_norm"] = self.normalize(
            df["career_years"]
        )

        df["education_norm"] = self.normalize(
            df["degree_score"]
        )

        df["behavior_norm"] = self.normalize(
            df["behavior_score"]
        )

        df["career_norm"] = self.normalize(
            df["career_stability_score"]
        )

        return df
    # ----------------------------------------------------
    # Skill Match
    # ----------------------------------------------------

    def skill_match_score(self, skills):

        candidate_skills = self.safe_set(skills)

        jd_skills = self.safe_set(self.jd["skills"])

        if len(jd_skills) == 0:
            return 0.0

        overlap = candidate_skills.intersection(jd_skills)

        return len(overlap) / len(jd_skills)

    # ----------------------------------------------------
    # Experience Match
    # ----------------------------------------------------

    def experience_fit_score(self, years):

        minimum = self.jd["minimum_experience"]
        maximum = self.jd["maximum_experience"]

        if minimum <= years <= maximum:
            return 1.0

        if years < minimum:

            gap = minimum - years

            return max(0.0, 1 - gap / minimum)

        gap = years - maximum

        return max(0.50, 1 - gap / 20)

    # ----------------------------------------------------
    # Title Match
    # ----------------------------------------------------

    def title_match_score(self, title):

        if not isinstance(title, str):
            return 0.0

        title = title.lower()

        if title in self.AI_TITLES:
            return 1.0

        for ai_title in self.AI_TITLES:

            if ai_title in title:
                return 0.9

        if "engineer" in title:
            return 0.60

        if "scientist" in title:
            return 0.75

        if "developer" in title:
            return 0.55

        if "analyst" in title:
            return 0.45

        return 0.10

    # ----------------------------------------------------
    # Education Match
    # ----------------------------------------------------

    def education_fit_score(self, row):

        score = row["education_norm"]

        if row["cs_related_degree"]:
            score += 0.25

        if row["ai_certification_count"] > 0:
            score += 0.10

        return min(score, 1.0)

    # ----------------------------------------------------
    # Apply Recruiter Scores
    # ----------------------------------------------------

    def calculate_component_scores(self):

        df = self.df

        df["skill_match"] = df["skills"].apply(
            self.skill_match_score
        )

        df["experience_match"] = df["career_years"].apply(
            self.experience_fit_score
        )

        df["title_match"] = df["current_title"].apply(
            self.title_match_score
        )

        df["education_match"] = df.apply(
            self.education_fit_score,
            axis=1
        )

        return df
    # ----------------------------------------------------
    # Technical Strength
    # ----------------------------------------------------

    def technical_score(self, row):

        score = 0.0

        score += row["ai_skill_count"] * 2.0
        score += row["vector_db_skill_count"] * 2.0
        score += row["mlops_skill_count"] * 1.5
        score += row["cloud_skill_count"] * 1.0
        score += row["backend_skill_count"] * 1.0
        score += row["data_engineering_skill_count"] * 1.5
        score += row["database_skill_count"] * 0.5
        score += row["programming_skill_count"] * 1.0

        score += row["ai_certification_count"] * 2.0
        score += row["cloud_certification_count"] * 1.0

        score += row["average_skill_assessment"] / 20

        return score

    # ----------------------------------------------------
    # Behaviour Score
    # ----------------------------------------------------

    def behavior_score(self, row):

        score = 0.0

        score += row["behavior_norm"] * 0.40

        score += row["github_activity_score"] / 10 * 0.15

        score += row["interview_completion_rate"] * 0.15

        score += row["offer_acceptance_rate"] * 0.10

        score += row["profile_completeness_score"] / 100 * 0.10

        score += row["recruiter_response_rate"] * 0.10

        if row["verified_email"]:
            score += 0.03

        if row["verified_phone"]:
            score += 0.03

        if row["linkedin_connected"]:
            score += 0.02

        return min(score, 1.0)

    # ----------------------------------------------------
    # Career Score
    # ----------------------------------------------------

    def career_score(self, row):

        score = row["career_norm"]

        score += min(row["company_count"] / 10, 0.15)

        score += min(row["career_years"] / 20, 0.20)

        score += min(row["avg_tenure_months"] / 60, 0.15)

        return min(score, 1.0)

    # ----------------------------------------------------
    # Location / Work Mode
    # ----------------------------------------------------

    def location_score(self, row):

        score = 0.0

        location = str(row["location"]).lower()

        preferred = self.jd["preferred_locations"]

        for city in preferred:

            if city in location:
                score += 0.60
                break

        if row["willing_to_relocate"]:
            score += 0.25

        if (
            self.jd["work_mode"] is not None
            and row["preferred_work_mode"] == self.jd["work_mode"]
        ):
            score += 0.15

        return min(score, 1.0)

    # ----------------------------------------------------
    # Calculate Remaining Scores
    # ----------------------------------------------------

    def calculate_remaining_scores(self):

        df = self.df

        df["technical_strength"] = df.apply(
            self.technical_score,
            axis=1
        )

        df["technical_strength"] = self.normalize(
            df["technical_strength"]
        )

        df["behavior_strength"] = df.apply(
            self.behavior_score,
            axis=1
        )

        df["career_strength"] = df.apply(
            self.career_score,
            axis=1
        )

        df["location_match"] = df.apply(
            self.location_score,
            axis=1
        )

        return df
    
    # ----------------------------------------------------
    # Final Weighted Score
    # ----------------------------------------------------

    def compute_final_score(self):

        df = self.df

        w = self.WEIGHTS

        df["final_score"] = (

            w["semantic"] * df["semantic_score"]

            + w["skills"] * df["skill_match"]

            + w["experience"] * df["experience_match"]

            + w["title"] * df["title_match"]

            + w["technical"] * df["technical_strength"]

            + w["education"] * df["education_match"]

            + w["behavior"] * df["behavior_strength"]

            + w["career"] * df["career_strength"]

            + w["location"] * df["location_match"]

        )

        return df

    # ----------------------------------------------------
    # Rank Candidates
    # ----------------------------------------------------

    def rank(self, top_k=100):

        self.normalize_features()

        self.calculate_component_scores()

        self.calculate_remaining_scores()

        self.compute_final_score()

        ranked = self.df.sort_values(
            "final_score",
            ascending=False,
        ).reset_index(drop=True)

        ranked["rank"] = ranked.index + 1

        return ranked.head(top_k)