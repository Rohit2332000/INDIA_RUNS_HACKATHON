"""
redrob_parser.py

Parses recruiter/activity signals from Redrob.
"""

from preprocessing.text_cleaner import TextCleaner


class RedrobParser:

    @staticmethod
    def _safe_float(value, default=0.0):
        try:
            if value is None:
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_int(value, default=0):
        try:
            if value is None:
                return default
            return int(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def parse(cls, candidate):

        rr = candidate.get("redrob_signals", {})

        recruiter_response_rate = cls._safe_float(
            rr.get("recruiter_response_rate")
        )

        github_activity_score = cls._safe_float(
            rr.get("github_activity_score")
        )

        interview_completion_rate = cls._safe_float(
            rr.get("interview_completion_rate")
        )

        offer_acceptance_rate = cls._safe_float(
            rr.get("offer_acceptance_rate")
        )

        profile_completeness_score = cls._safe_float(
            rr.get("profile_completeness_score")
        )

        search_appearance_30d = cls._safe_int(
            rr.get("search_appearance_30d")
        )

        saved_by_recruiters_30d = cls._safe_int(
            rr.get("saved_by_recruiters_30d")
        )

        profile_views_received_30d = cls._safe_int(
            rr.get("profile_views_received_30d")
        )

        connection_count = cls._safe_int(
            rr.get("connection_count")
        )

        endorsements_received = cls._safe_int(
            rr.get("endorsements_received")
        )

        applications_submitted_30d = cls._safe_int(
            rr.get("applications_submitted_30d")
        )

        avg_response_time_hours = cls._safe_float(
            rr.get("avg_response_time_hours")
        )

        notice_period_days = cls._safe_int(
            rr.get("notice_period_days")
        )

        open_to_work = bool(
            rr.get("open_to_work_flag", False)
        )

        willing_to_relocate = bool(
            rr.get("willing_to_relocate", False)
        )

        linkedin_connected = bool(
            rr.get("linkedin_connected", False)
        )

        preferred_work_mode = TextCleaner.clean_text(
            rr.get("preferred_work_mode", "")
        )

        verified_email = bool(
            rr.get("verified_email", False)
        )

        verified_phone = bool(
            rr.get("verified_phone", False)
        )

        salary = rr.get("expected_salary_range_inr_lpa", {})

        expected_salary_min = cls._safe_float(
            salary.get("min")
        )

        expected_salary_max = cls._safe_float(
            salary.get("max")
        )

        assessment_scores = rr.get(
            "skill_assessment_scores", {}
        )

        average_skill_assessment = (
            round(
                sum(assessment_scores.values()) /
                len(assessment_scores),
                2,
            )
            if assessment_scores
            else 0
        )

        behavior_score = round(
            (
                recruiter_response_rate * 0.20
                + interview_completion_rate * 0.20
                + offer_acceptance_rate * 0.15
                + (profile_completeness_score / 100) * 0.15
                + (github_activity_score / 10) * 0.15
                + (average_skill_assessment / 100) * 0.15
            ),
            3,
        )

        return {

            "recruiter_response_rate": recruiter_response_rate,

            "github_activity_score": github_activity_score,

            "interview_completion_rate": interview_completion_rate,

            "offer_acceptance_rate": offer_acceptance_rate,

            "profile_completeness_score": profile_completeness_score,

            "search_appearance_30d": search_appearance_30d,

            "saved_by_recruiters_30d": saved_by_recruiters_30d,

            "profile_views_received_30d": profile_views_received_30d,

            "connection_count": connection_count,

            "endorsements_received": endorsements_received,

            "applications_submitted_30d": applications_submitted_30d,

            "avg_response_time_hours": avg_response_time_hours,

            "notice_period_days": notice_period_days,

            "open_to_work": open_to_work,

            "willing_to_relocate": willing_to_relocate,

            "linkedin_connected": linkedin_connected,

            "preferred_work_mode": preferred_work_mode,

            "verified_email": verified_email,

            "verified_phone": verified_phone,

            "expected_salary_min": expected_salary_min,

            "expected_salary_max": expected_salary_max,

            "average_skill_assessment": average_skill_assessment,

            "behavior_score": behavior_score,

            "behavior_text": (
                f"Recruiter response {recruiter_response_rate}, "
                f"GitHub {github_activity_score}, "
                f"Interview completion {interview_completion_rate}, "
                f"Profile completeness {profile_completeness_score}, "
                f"Assessment {average_skill_assessment}"
            ),
        }