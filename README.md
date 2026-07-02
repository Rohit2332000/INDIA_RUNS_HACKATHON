# 🤖 RecruitRankAI

### AI-Powered Candidate Ranking System for Intelligent Hiring

> **RecruitRankAI** is an end-to-end AI-powered candidate ranking platform that leverages semantic search, hybrid ranking, feature engineering, and explainable AI to help recruiters identify the most relevant candidates from large talent pools.

---

## 🚀 Project Overview

RecruitRankAI automates the candidate screening process by combining **Natural Language Processing**, **Sentence Transformers**, **FAISS semantic retrieval**, and a **hybrid ranking algorithm**.

Given a Job Description (JD), the system:

* Parses recruiter requirements
* Extracts structured candidate features
* Generates semantic embeddings
* Retrieves the most relevant candidates using FAISS
* Applies a hybrid scoring algorithm
* Produces an explainable ranked CSV for recruiters

The project is designed to be **reproducible**, **scalable**, and **easy to evaluate** through a Streamlit sandbox.

---

# ✨ Features

* 📄 Automatic Job Description Parsing
* 👤 Candidate Profile Feature Engineering
* 🧠 Semantic Search using Sentence Transformers
* ⚡ FAISS Vector Similarity Search
* 📊 Hybrid Ranking Algorithm
* 💬 Explainable Candidate Reasoning
* 📥 Downloadable Ranked CSV
* 🌐 Interactive Streamlit Demo
* 🔁 Fully Reproducible Pipeline

---

# 🏗️ System Architecture

```text
                    Job Description
                           │
                           ▼
                    JD Parser
                           │
                           ▼
                Sentence Transformer
                           │
                           ▼
                  JD Embedding Vector
                           │
                           ▼
                 FAISS Similarity Search
                           │
                           ▼
          Top Semantic Candidate Retrieval
                           │
                           ▼
               Hybrid Ranking Algorithm
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
     Skill Match     Experience Fit    Technical Score
          │                │                 │
          └────────────────┼─────────────────┘
                           │
                           ▼
                   Final Candidate Score
                           │
                           ▼
             Explainable Recruiter Reasoning
                           │
                           ▼
              Ranked Candidate CSV Output
```

---

# 🛠️ Tech Stack

### Programming

* Python

### Machine Learning & AI

* Sentence Transformers
* Transformers
* PyTorch

### Vector Search

* FAISS

### Data Processing

* Pandas
* NumPy
* PyArrow

### Web Application

* Streamlit

### Utilities

* tqdm

---

# 📂 Project Structure

```text
RecruitRankAI/
│
├── app/
├── config/
├── data/
├── embeddings/
├── feature_engineering/
├── features/
├── index/
├── jd/
├── output/
├── pipeline/
├── preprocessing/
├── ranking/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── Dockerfile (optional)
```

---

# ⚙️ Ranking Pipeline

The ranking process consists of the following stages:

### 1. Candidate Preprocessing

Extracts structured information including:

* Skills
* Experience
* Education
* Certifications
* Languages
* Career Information
* Recruiter Behaviour Metrics

---

### 2. Feature Engineering

Creates numerical features such as:

* AI Skill Count
* Cloud Skill Count
* Backend Skill Count
* Degree Score
* Career Stability
* Behaviour Score
* Profile Completeness
* Recruiter Response Rate

---

### 3. Embedding Generation

Candidate profiles are converted into semantic vectors using:

**sentence-transformers/all-MiniLM-L6-v2**

---

### 4. FAISS Vector Search

Performs efficient semantic retrieval of the most relevant candidates using cosine similarity.

---

### 5. Hybrid Ranking

Final ranking combines:

| Component           | Description                                 |
| ------------------- | ------------------------------------------- |
| Semantic Similarity | Semantic relevance between JD and candidate |
| Skill Match         | Overlap between candidate and JD skills     |
| Experience Fit      | Matching required experience                |
| Technical Strength  | Technical capability score                  |
| Education           | Educational relevance                       |
| Behaviour           | Platform engagement & recruiter metrics     |
| Career Stability    | Employment consistency                      |
| Location Match      | Preferred location & work mode              |

---

### 6. Explainable AI

Each ranked candidate includes recruiter-friendly reasoning such as:

* Strong semantic similarity
* Relevant AI skills
* Strong cloud platform experience
* Computer Science background
* Stable career progression
* Experience with vector databases

---

# 📊 Sample Output

| Rank | Candidate ID |  Score |
| ---: | ------------ | -----: |
|    1 | CAND_0000031 | 0.5875 |
|    2 | CAND_0000001 | 0.4986 |
|    3 | CAND_0000094 | 0.4983 |
|    4 | CAND_0000058 | 0.4982 |
|    5 | CAND_0000060 | 0.4981 |

Generated output format:

```csv
candidate_id,rank,score,reasoning
CAND_0000031,1,0.5875,...
...
```

---

# 🌐 Streamlit Demo

The Streamlit application allows users to:

* Load a preloaded candidate dataset (≤100 candidates)
* Upload or paste a Job Description
* Execute the complete ranking pipeline
* View ranked candidates
* Download the ranked CSV

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/RecruitRankAI.git

cd RecruitRankAI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Pipeline

## 1. Preprocess Candidates

```bash
python -m preprocessing.preprocess_candidates
```

---

## 2. Generate Candidate Embeddings

```bash
python -m embeddings.build_candidate_embeddings
```

---

## 3. Build FAISS Index

```bash
python -m embeddings.vector_store
```

---

## 4. Run End-to-End Ranking

```bash
python -m pipeline.inference
```

Generated output:

```text
output/submission.csv
```

---

# ▶️ Running Streamlit

```bash
streamlit run streamlit_app.py
```

---

# 📦 Sandbox

**Live Streamlit Demo**

> Add your deployed Streamlit URL here

```text
https://your-app.streamlit.app
```

---

# 📈 Performance

* Supports semantic retrieval using FAISS
* CPU-friendly inference
* Suitable for ≤100 candidates in Streamlit sandbox
* End-to-end execution completes within minutes on CPU

---

# 📋 Submission Checklist

* ✅ Public GitHub Repository
* ✅ Streamlit Sandbox
* ✅ Ranked CSV (100 candidates)
* ✅ Project Report / PDF
* ✅ Reproducible Codebase
* ✅ requirements.txt included
* ✅ README documentation

---

# 🔮 Future Improvements

* Learning-to-Rank (LTR) models
* Cross-Encoder re-ranking
* Personalized recruiter preferences
* LLM-based reasoning generation
* Resume PDF parsing
* Multi-job ranking
* Real-time ATS integration
* Cloud deployment with APIs

---

# 👨‍💻 Author

**Rohit Kumar Yadav**

AI | Machine Learning | GenAI | NLP | Information Retrieval

---

# 📄 License

This project is developed for the **Redrob AI Hiring Challenge** as a demonstration of AI-powered candidate ranking and semantic retrieval.
