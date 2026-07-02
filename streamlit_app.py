"""
RecruitRankAI
Streamlit Demo
"""

import pandas as pd
import streamlit as st

from config.config import (
    FEATURE_CSV,
    JOB_DESCRIPTION_FILE
)

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="RecruitRankAI",
    page_icon="🤖",
    layout="wide"
)

# ==========================================================
# Load Dataset
# ==========================================================

try:

    candidates = pd.read_csv(FEATURE_CSV)

except Exception as e:

    st.error(f"Unable to load candidate features.\n\n{e}")
    st.stop()

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("RecruitRankAI")

st.sidebar.success("Dataset Loaded")

st.sidebar.metric(
    "Candidates",
    len(candidates)
)

st.sidebar.metric(
    "Features",
    len(candidates.columns)
)

st.sidebar.markdown("---")

st.sidebar.write("### Pipeline")

st.sidebar.write("✔ Feature Engineering")
st.sidebar.write("✔ Sentence Transformers")
st.sidebar.write("✔ FAISS Retrieval")
st.sidebar.write("✔ Hybrid Ranking")
st.sidebar.write("✔ Explainable AI")

# ==========================================================
# Header
# ==========================================================

st.title("🤖 RecruitRankAI")

st.caption(
    "AI Powered Candidate Ranking System"
)

st.markdown("---")

# ==========================================================
# Candidate Preview
# ==========================================================

with st.expander("Candidate Dataset"):

    st.dataframe(
        candidates.head(),
        use_container_width=True
    )

# ==========================================================
# Job Description
# ==========================================================

st.subheader("Job Description")

col1, col2 = st.columns(2)

with col1:

    uploaded_file = st.file_uploader(
        "Upload Job Description",
        type=["txt"]
    )

with col2:

    jd = st.text_area(
        "Or Paste Job Description",
        height=300
    )

# ==========================================================
# Default JD
# ==========================================================

if st.button("Load Default JD"):

    try:

        with open(JOB_DESCRIPTION_FILE, "r", encoding="utf-8") as f:

            st.session_state["jd"] = f.read()

    except:

        st.error("Default JD not found.")

if "jd" in st.session_state:

    jd = st.session_state["jd"]

    st.text_area(
        "Loaded JD",
        jd,
        height=300
    )

# ==========================================================
# Run
# ==========================================================

# ==========================================================
# Run
# ==========================================================

import os
import subprocess

from config.config import SUBMISSION_FILE

st.markdown("---")

if st.button(
    "🚀 Rank Candidates",
    use_container_width=True
):

    if uploaded_file is not None:
        jd = uploaded_file.read().decode()

    if jd.strip() == "":
        st.warning("Please upload or paste a Job Description.")
        st.stop()

    # Save uploaded JD
    with open(JOB_DESCRIPTION_FILE, "w", encoding="utf-8") as f:
        f.write(jd)

    st.success("Job Description Saved")

    with st.spinner("Running RecruitRankAI..."):

        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            text=True
        )

    if result.returncode != 0:

        st.error(result.stderr)

    else:

        st.success("Ranking Complete!")

        if os.path.exists(SUBMISSION_FILE):

            submission = pd.read_csv(SUBMISSION_FILE)

            st.subheader("Top Candidates")

            st.dataframe(
                submission,
                use_container_width=True
            )

            with open(SUBMISSION_FILE, "rb") as f:

                st.download_button(
                    "📥 Download submission.csv",
                    data=f,
                    file_name="submission.csv",
                    mime="text/csv"
                )

        else:

            st.error("submission.csv not found.")
# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    "RecruitRankAI | Redrob AI Hiring Challenge"
)