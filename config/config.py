"""
Global configuration for RecruitRankAI
"""

from pathlib import Path

# -------------------------------------------------------
# Root Directory
# -------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# Data
# -------------------------------------------------------

DATA_DIR = ROOT_DIR / "data"

CANDIDATE_FILE = DATA_DIR / "candidates.jsonl"
JOB_DESCRIPTION_FILE = DATA_DIR / "job_description.txt"

# -------------------------------------------------------
# Features
# -------------------------------------------------------

FEATURE_DIR = ROOT_DIR / "features"

FEATURE_FILE = FEATURE_DIR / "candidate_features.parquet"
FEATURE_FILE = FEATURE_DIR / "candidate_features.parquet"
FEATURE_CSV = FEATURE_DIR / "candidate_features.csv"

# -------------------------------------------------------
# Embeddings
# -------------------------------------------------------

INDEX_DIR = ROOT_DIR / "index"

EMBEDDING_FILE = INDEX_DIR / "candidate_embeddings.npy"

FAISS_INDEX = INDEX_DIR / "faiss.index"

# -------------------------------------------------------
# Output
# -------------------------------------------------------

OUTPUT_DIR = ROOT_DIR / "output"

SUBMISSION_FILE = OUTPUT_DIR / "submission1.csv"

# -------------------------------------------------------
# Embedding Model
# -------------------------------------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# -------------------------------------------------------
# Retrieval
# -------------------------------------------------------

TOP_K_RETRIEVAL = 500

TOP_K_SUBMISSION = 100