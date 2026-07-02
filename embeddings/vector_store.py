"""
vector_store.py

Builds and loads a FAISS index for semantic candidate retrieval.
"""

import faiss
import numpy as np

from config.config import (
    EMBEDDING_FILE,
    FAISS_INDEX,
)


class VectorStore:

    @staticmethod
    def build():

        print("\nLoading candidate embeddings...")

        embeddings = np.load(EMBEDDING_FILE)

        dimension = embeddings.shape[1]

        print(f"Embedding Dimension : {dimension}")
        print(f"Candidates          : {len(embeddings)}")

        # Since embeddings are normalized,
        # Inner Product == Cosine Similarity
        index = faiss.IndexFlatIP(dimension)

        index.add(embeddings)

        faiss.write_index(index, str(FAISS_INDEX))

        print("\nFAISS Index Saved")
        print(FAISS_INDEX)

    @staticmethod
    def load():

        return faiss.read_index(str(FAISS_INDEX))
        

def main():

    VectorStore.build()


if __name__ == "__main__":
    main()