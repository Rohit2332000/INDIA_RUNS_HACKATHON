"""
candidate_document.py

Creates a rich textual representation of a candidate.
This document will later be embedded using BGE for semantic retrieval.
"""

import numpy as np
import pandas as pd


class CandidateDocumentBuilder:

    @staticmethod
    def _join(values):
        """
        Safely converts lists, tuples, numpy arrays and scalars
        into comma-separated text.
        """

        if values is None:
            return "None"

        # Handle NaN
        if isinstance(values, float) and pd.isna(values):
            return "None"

        # Convert numpy arrays -> list
        if isinstance(values, np.ndarray):
            values = values.tolist()

        # Handle list/tuple
        if isinstance(values, (list, tuple)):
            cleaned = [
                str(v).strip()
                for v in values
                if str(v).strip()
            ]

            return ", ".join(cleaned) if cleaned else "None"

        value = str(values).strip()

        return value if value else "None"

    @classmethod
    def build(cls, row):

        sections = []

        # --------------------------------------------------
        # Candidate
        # --------------------------------------------------

        sections.append(
            f"Candidate ID: {row.get('candidate_id', '')}"
        )

        # --------------------------------------------------
        # Profile
        # --------------------------------------------------

        sections.append(f"""
================ PROFILE ================

Current Position:
{row.get('current_title', '')}

Headline:
{row.get('headline', '')}

Experience:
{row.get('years_experience', 0)} years

Industry:
{row.get('current_industry', '')}

Company:
{row.get('current_company', '')}

Location:
{row.get('location', '')}, {row.get('country', '')}
""")

        # --------------------------------------------------
        # Career
        # --------------------------------------------------

        sections.append(f"""
================ CAREER ================

Career Years:
{row.get('career_years', 0)}

Jobs:
{row.get('job_count', 0)}

Companies:
{cls._join(row.get('companies'))}

Titles:
{cls._join(row.get('titles'))}

Industries:
{cls._join(row.get('industries'))}
""")

        # --------------------------------------------------
        # Education
        # --------------------------------------------------

        sections.append(f"""
================ EDUCATION ================

Highest Degree:
{row.get('highest_degree', '')}

Degree Score:
{row.get('degree_score', 0)}

Computer Science Degree:
{row.get('cs_related_degree', False)}

Institutions:
{cls._join(row.get('institutions'))}

Fields:
{cls._join(row.get('fields'))}
""")

        # --------------------------------------------------
        # Skills
        # --------------------------------------------------

        sections.append(f"""
================ SKILLS ================

All Skills:
{cls._join(row.get('skills'))}

AI Skills:
{cls._join(row.get('ai_skills'))}

Programming:
{cls._join(row.get('programming_skills'))}

Cloud:
{cls._join(row.get('cloud_skills'))}

Database:
{cls._join(row.get('database_skills'))}

Backend:
{cls._join(row.get('backend_skills'))}

Frontend:
{cls._join(row.get('frontend_skills'))}

Data Engineering:
{cls._join(row.get('data_engineering_skills'))}

MLOps:
{cls._join(row.get('mlops_skills'))}

Vector Databases:
{cls._join(row.get('vector_db_skills'))}
""")

        # --------------------------------------------------
        # Certifications
        # --------------------------------------------------

        sections.append(f"""
================ CERTIFICATIONS ================

{cls._join(row.get('certifications'))}
""")

        # --------------------------------------------------
        # Languages
        # --------------------------------------------------

        sections.append(f"""
================ LANGUAGES ================

Languages:
{cls._join(row.get('languages'))}
""")

        # --------------------------------------------------
        # Recruiter Signals
        # --------------------------------------------------

        sections.append(f"""
================ RECRUITER SIGNALS ================

Recruiter Response Rate:
{row.get('recruiter_response_rate', 0)}

GitHub Activity:
{row.get('github_activity_score', 0)}

Interview Completion:
{row.get('interview_completion_rate', 0)}

Offer Acceptance:
{row.get('offer_acceptance_rate', 0)}

Behavior Score:
{row.get('behavior_score', 0)}

Profile Completeness:
{row.get('profile_completeness_score', 0)}

Search Appearance:
{row.get('search_appearance_30d', 0)}

Saved By Recruiters:
{row.get('saved_by_recruiters_30d', 0)}

Profile Views:
{row.get('profile_views_received_30d', 0)}

Connections:
{row.get('connection_count', 0)}
""")

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        sections.append(f"""
================ SUMMARY ================

{row.get('summary', '')}
""")

        return "\n".join(sections)