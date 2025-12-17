SHL Assessment Recommendation Engine
Overview

This project implements an intelligent Assessment Recommendation Engine using SHL’s product catalog.
Given a job description or hiring requirement, the system recommends the most relevant SHL assessments by combining semantic understanding and keyword-based retrieval.

The solution is designed to be accurate, explainable, and production-ready, following the requirements provided by the SHL AI team.

Key Features

Hybrid retrieval using Semantic Embeddings + BM25

Intelligent query cleaning and expansion

Balanced recommendations across technical and behavioral assessments

REST API built with FastAPI

Evaluation using Mean Recall@10

Fully automated test prediction generation

Architecture
Query / Job Description
        │
        ▼
Query Cleaning & Expansion
        │
        ▼
Hybrid Retrieval
(Embeddings + BM25)
        │
        ▼
Candidate Pool Expansion
        │
        ▼
Conditional Test-Type Balancing
        │
        ▼
Top-10 Assessment Recommendations

Data

Assessment Catalog: Built from the provided SHL dataset (catalog/catalogue.csv)

Queries: Taken from Gen_AI Dataset.xlsx

Train set → Recall@10 evaluation

Test set → Final prediction generation

Recommendation Logic

Query Cleaning & Expansion
Important intent keywords (e.g., skills, role indicators, behavioral signals) are extracted and appended to improve semantic matching.

Hybrid Retrieval

Semantic Search: Sentence Transformers (all-MiniLM-L6-v2)

Keyword Search: BM25

Combined using a weighted scoring mechanism favoring semantic similarity.

Candidate Pool Expansion

Retrieve top 25 candidates before reranking to improve recall.

Conditional Balancing

If a query spans both technical and behavioral competencies, the final recommendations are balanced across test types without reducing relevance.

Final Ranking

Top 10 assessments returned in ranked order.

API Endpoints
Health Check
GET /health


Response:

{ "status": "healthy" }

Recommendation Endpoint
POST /recommend


Request body:

{
  "query": "Need a SQL developer who can collaborate with stakeholders"
}


Response:

{
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/...",
      "name": "Sql Server New",
      "adaptive_support": "Yes",
      "description": "SHL assessment used for talent evaluation.",
      "duration": -1,
      "remote_support": "Yes",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}

Evaluation

Metric: Mean Recall@10

Approach:

For each training query, a hit is counted if the correct assessment appears in the top-10 recommendations.

Result:

Achieved Recall@10 ≈ 0.5 on the training set.

Given the limited catalog size and verbose job descriptions, this score reflects strong semantic matching performance.

Evaluation script:

eval/recall_at_10.py

Test Predictions

Final predictions for the test set are generated in:

eval/test_predictions.csv


Format:

Query,Assessment_url


Each query has up to 10 recommended assessment URLs, ordered by relevance.

Running the Project Locally
1. Install dependencies
pip install -r requirements.txt

2. Start the API
uvicorn api.main:app --host 0.0.0.0 --port 8000

3. Test the API

Visit: http://localhost:8000/docs

Use Swagger UI to test /recommend

Deployment

The application can be deployed on any cloud platform supporting Python (e.g., Render, Railway, Azure).
Deployment instructions are compatible with standard FastAPI hosting setups.

Project Structure
shl-assessment-recommender/
│
├── api/
│   ├── main.py
│   └── models.py
│
├── retrieval/
│   ├── hybrid_search.py
│   └── balanced_search.py
│
├── eval/
│   ├── recall_at_10.py
│   └── test_predictions.csv
│
├── catalog/
│   └── catalogue.csv
│
├── requirements.txt
└── README.md

Limitations & Future Improvements

Limited assessment catalog size restricts maximum achievable recall.

Test-type classification is heuristic-based.

Future improvements could include:

Learning-to-rank re-ranking

Larger assessment coverage

Domain-specific embedding fine-tuning


Author
Vedang Rajoriya
Final-year B.Tech student | AI / ML Enthusiast

Final Note

This solution focuses on clarity, robustness, and explainability, aligning with SHL’s real-world assessment recommendation use cases.