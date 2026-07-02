"""
build_candidate_embeddings.py

Generates semantic embeddings for every candidate profile.
"""

import numpy as np
import pandas as pd

from tqdm import tqdm

from config.config import (
    FEATURE_FILE,
    EMBEDDING_FILE,
)

from embeddings.embedding_model import EmbeddingModel
from feature_engineering.candidate_document import (
    CandidateDocumentBuilder,
)


class CandidateEmbeddingBuilder:

    def __init__(self):

        self.model = EmbeddingModel()

    def load_candidates(self):

        print("\nLoading candidate features...")

        df = pd.read_parquet(FEATURE_FILE)

        print(f"{len(df)} candidates loaded.\n")

        return df

    def build_documents(self, df):

        print("Creating candidate documents...")

        documents = []

        for _, row in tqdm(df.iterrows(), total=len(df)):

            documents.append(
                CandidateDocumentBuilder.build(row)
            )

        return documents

    def generate_embeddings(self, documents):

        print("\nGenerating embeddings...\n")

        embeddings = self.model.encode(
            documents,
            batch_size=64,
            normalize=True,
        )

        return embeddings

    def save(self, embeddings):

        np.save(
            EMBEDDING_FILE,
            embeddings,
        )

        print("\nEmbeddings saved to:")
        print(EMBEDDING_FILE)

        print("\nEmbedding Shape:")
        print(embeddings.shape)


def main():

    builder = CandidateEmbeddingBuilder()

    df = builder.load_candidates()

    docs = builder.build_documents(df)

    embeddings = builder.generate_embeddings(docs)

    builder.save(embeddings)


if __name__ == "__main__":

    main()