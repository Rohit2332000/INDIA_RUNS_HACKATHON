"""
semantic_search.py

Retrieves the most semantically relevant candidates
using the FAISS index.
"""

import pandas as pd

from config.config import (
    FEATURE_FILE,
    TOP_K_RETRIEVAL,
)

from embeddings.vector_store import VectorStore
from jd.jd_embedding import JDEmbeddingBuilder


class SemanticSearch:

    def __init__(self):

        self.index = VectorStore.load()

        self.df = pd.read_parquet(FEATURE_FILE)

    def search(self, top_k=TOP_K_RETRIEVAL):

        # -----------------------
        # JD Embedding
        # -----------------------

        jd = JDEmbeddingBuilder.get_embedding()

        query = jd["embedding"].reshape(1, -1)

        # -----------------------
        # FAISS Search
        # -----------------------

        scores, indices = self.index.search(
            query,
            min(top_k, len(self.df))
        )

        print("=" * 60)
        print("Rows in dataframe:", len(self.df))
        print("FAISS returned:", len(indices[0]))
        print("Unique indices:", len(set(indices[0])))
        print("Min index:", indices[0].min())
        print("Max index:", indices[0].max())
        print("Last 10 indices:", indices[0][-10:])
        print("Last 10 scores:", scores[0][-10:])
        print("=" * 60)
        results = self.df.iloc[indices[0]].copy()

        results["semantic_score"] = scores[0]

        results = results.sort_values(
            "semantic_score",
            ascending=False,
        )

        return results.reset_index(drop=True)