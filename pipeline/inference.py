"""
End-to-End RecruitRankAI Pipeline
"""

import pandas as pd

from config.config import SUBMISSION_FILE

from ranking.hybrid_ranker import HybridRanker
from ranking.reasoning_generator import ReasoningGenerator


def run_pipeline(top_k=100):

    print("=" * 60)
    print("RecruitRankAI Pipeline")
    print("=" * 60)

    # ---------------------------------------------------
    # Hybrid Ranking
    # ---------------------------------------------------

    print("Ranking candidates...")

    ranker = HybridRanker()

    ranked = ranker.rank(top_k)

    # ---------------------------------------------------
    # Generate Reasons
    # ---------------------------------------------------

    print("Generating recruiter explanations...")

    ranked["reasoning"] = ranked.apply(
        ReasoningGenerator.generate,
        axis=1
    )

    # ---------------------------------------------------
    # Final Submission
    # ---------------------------------------------------

    submission = ranked[
        [
            "candidate_id",
            "rank",
            "final_score",
            "reasoning",
        ]
    ].copy()

    submission.rename(
        columns={
            "final_score": "score"
        },
        inplace=True,
    )

    submission.to_csv(
        SUBMISSION_FILE,
        index=False,
    )

    print()

    print("Submission Saved")

    print(SUBMISSION_FILE)

    print()

    print(submission.head(10))

    return submission


if __name__ == "__main__":

    run_pipeline()