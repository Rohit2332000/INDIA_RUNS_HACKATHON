"""
preprocess_candidates.py

Master preprocessing pipeline for RecruitRankAI.

Loads raw candidate JSON, extracts structured features using all
parsers, validates records, removes duplicates and saves the final
feature dataset.
"""

import json
import pandas as pd
from tqdm import tqdm

from config.config import (
    CANDIDATE_FILE,
    FEATURE_FILE,
    FEATURE_CSV,
    FEATURE_DIR,
)

from preprocessing.profile_parser import ProfileParser
from preprocessing.career_parser import CareerParser
from preprocessing.education_parser import EducationParser
from preprocessing.skills_parser import SkillsParser
from preprocessing.certification_parser import CertificationParser
from preprocessing.language_parser import LanguageParser
from preprocessing.redrob_parser import RedrobParser


class CandidatePreprocessor:

    def __init__(self):
        self.records = []

    def process_candidate(self, candidate):

        record = {
            "candidate_id": candidate.get("candidate_id")
        }

        record.update(ProfileParser.parse(candidate))
        record.update(CareerParser.parse(candidate))
        record.update(EducationParser.parse(candidate))
        record.update(SkillsParser.parse(candidate))
        record.update(CertificationParser.parse(candidate))
        record.update(LanguageParser.parse(candidate))
        record.update(RedrobParser.parse(candidate))

        return record

    def load_candidates(self):

        print("=" * 60)
        print("Loading Candidate Dataset")
        print("=" * 60)

        with open(CANDIDATE_FILE, "r", encoding="utf-8") as f:
            candidates = json.load(f)

        print(f"Total Candidates : {len(candidates):,}\n")

        for candidate in tqdm(candidates):

            try:
                self.records.append(
                    self.process_candidate(candidate)
                )

            except Exception as e:
                print(
                    f"Skipping {candidate.get('candidate_id')} -> {e}"
                )

    def build_dataframe(self):

        df = pd.DataFrame(self.records)

        before = len(df)

        df = df.drop_duplicates(
            subset="candidate_id"
        ).reset_index(drop=True)

        after = len(df)

        print("\nDuplicate Records Removed :", before - after)

        return df

    def save(self, df):

        FEATURE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_parquet(
            FEATURE_FILE,
            index=False,
        )

        df.to_csv(
            FEATURE_CSV,
            index=False,
        )

        print("\n" + "=" * 60)
        print("Preprocessing Completed")
        print("=" * 60)
        print(f"Candidates : {len(df):,}")
        print(f"Features   : {df.shape[1]}")
        print(f"\nSaved:")
        print(FEATURE_FILE)
        print(FEATURE_CSV)
        print("=" * 60)


def main():

    processor = CandidatePreprocessor()

    processor.load_candidates()

    df = processor.build_dataframe()

    processor.save(df)


if __name__ == "__main__":
    main()