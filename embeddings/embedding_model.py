"""
embedding_model.py

Loads the embedding model used throughout RecruitRankAI.
"""

from sentence_transformers import SentenceTransformer

from config.config import EMBEDDING_MODEL


class EmbeddingModel:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print(f"\nLoading embedding model: {EMBEDDING_MODEL}")

            cls._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        return cls._model

    @classmethod
    def encode(
        cls,
        texts,
        batch_size=64,
        normalize=True,
    ):

        model = cls.get_model()

        return model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=normalize,
            convert_to_numpy=True,
        )