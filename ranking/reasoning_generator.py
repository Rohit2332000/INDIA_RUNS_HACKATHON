"""
reasoning_generator.py

Generate recruiter-style explanations for why a candidate
was ranked.

These reasons are later written to submission.csv.
"""


class ReasoningGenerator:

    @staticmethod
    def generate(row):

        reasons = []

        # --------------------------------------------
        # Semantic Match
        # --------------------------------------------

        if row["semantic_score"] >= 0.70:
            reasons.append("Excellent semantic match with the job description.")

        elif row["semantic_score"] >= 0.55:
            reasons.append("Strong semantic similarity to the required role.")

        elif row["semantic_score"] >= 0.40:
            reasons.append("Moderate semantic relevance.")

        # --------------------------------------------
        # Skills
        # --------------------------------------------

        if row["skill_match"] >= 0.80:
            reasons.append("Matches most of the required technical skills.")

        elif row["skill_match"] >= 0.50:
            reasons.append("Good overlap with required technical skills.")

        elif row["ai_skill_count"] >= 5:
            reasons.append("Strong AI and Machine Learning skillset.")

        elif row["ai_skill_count"] >= 2:
            reasons.append("Relevant AI skills present.")

        # --------------------------------------------
        # Experience
        # --------------------------------------------

        if row["experience_match"] >= 0.95:
            reasons.append(
                f"{row['career_years']:.1f} years of relevant experience."
            )

        elif row["career_years"] >= 10:
            reasons.append("Extensive industry experience.")

        # --------------------------------------------
        # Title
        # --------------------------------------------

        if row["title_match"] >= 0.90:
            reasons.append(
                f"Current role ({row['current_title']}) is highly relevant."
            )

        # --------------------------------------------
        # Education
        # --------------------------------------------

        if row["cs_related_degree"]:
            reasons.append("Computer Science related educational background.")

        # --------------------------------------------
        # Technical
        # --------------------------------------------

        if row["technical_strength"] >= 0.80:
            reasons.append("Strong technical profile.")

        # --------------------------------------------
        # Behaviour
        # --------------------------------------------

        if row["behavior_strength"] >= 0.80:
            reasons.append("Excellent recruiter and platform engagement.")

        elif row["behavior_strength"] >= 0.60:
            reasons.append("Good professional activity.")

        # --------------------------------------------
        # Career
        # --------------------------------------------

        if row["career_strength"] >= 0.80:
            reasons.append("Stable career progression.")

        # --------------------------------------------
        # Certifications
        # --------------------------------------------

        if row["ai_certification_count"] > 0:
            reasons.append("Relevant AI certifications.")

        # --------------------------------------------
        # Cloud
        # --------------------------------------------

        if row["cloud_skill_count"] >= 2:
            reasons.append("Strong cloud platform experience.")

        # --------------------------------------------
        # Vector DB
        # --------------------------------------------

        if row["vector_db_skill_count"] > 0:
            reasons.append("Experience with vector databases.")

        # --------------------------------------------
        # Fallback
        # --------------------------------------------

        if not reasons:
            reasons.append("General profile relevance.")

        return " ".join(reasons)