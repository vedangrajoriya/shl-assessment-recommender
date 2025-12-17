# SHL Assessment Recommendation Engine

## Overview
This repository contains an intelligent **Assessment Recommendation Engine** built using SHL’s product catalog.  
Given a job description or hiring requirement, the system recommends the **most relevant SHL assessments** using a hybrid information retrieval approach.

The solution is designed to be **accurate, explainable, and production-ready**, in line with the requirements shared by the SHL AI team.

---

## Key Features
- Hybrid retrieval using **Semantic Embeddings + BM25**
- Query cleaning and lightweight expansion for better intent capture
- Conditional balancing across **technical** and **behavioral** assessments
- REST API built with **FastAPI**
- Evaluation using **Mean Recall@10**
- Automated generation of test predictions

---

## System Architecture

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



---

## Data
- **Assessment Catalog**: Built from the provided SHL dataset  
  - `catalog/catalogue.csv`
- **Queries**: From `Gen_AI Dataset.xlsx`
  - Training set → Recall@10 evaluation
  - Test set → Final prediction generation

---

## Recommendation Logic

1. **Query Cleaning & Expansion**  
   Extracts important intent keywords (skills, role indicators, behavioral signals) to improve semantic matching.

2. **Hybrid Retrieval**
   - Semantic similarity using Sentence Transformers (`all-MiniLM-L6-v2`)
   - Keyword relevance using BM25
   - Combined using weighted scoring favoring semantic similarity.

3. **Candidate Pool Expansion**
   - Retrieves a larger candidate set (top 25) before reranking to improve recall.

4. **Conditional Balancing**
   - Ensures a balanced mix of technical and behavioral assessments when required.

5. **Final Ranking**
   - Returns the top 10 assessments ordered by relevance.

---

## API Endpoints

### Health Check
GET /health


Response:
```json
{ "status": "healthy" }
Recommendation Endpoint



POST /recommend
Request body:
{
  "query": "Need a SQL developer who can collaborate with stakeholders"
}

Response (example):


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

Methodology:

A hit is counted if the correct assessment appears in the top-10 recommendations for a query.

Result:

Achieved Recall@10 ≈ 0.5 on the training set.

Evaluation script:

eval/recall_at_10.py
Test Predictions

Final predictions for the test set are stored in:
eval/test_predictions.csv

CSV format:
Query,Assessment_url
Each query has up to 10 recommended assessment URLs, ordered by relevance.

Running the Project Locally
Install dependencies

pip install -r requirements.txt
Start the API

uvicorn api.main:app --host 0.0.0.0 --port 8000
Test the API
Open: http://localhost:8000/docs

Use Swagger UI to test /recommend

Deployment
The API can be deployed on any cloud platform supporting Python and FastAPI (e.g., Render, Railway, Azure).
Deployment instructions are compatible with standard FastAPI hosting workflows.

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

Test-type classification uses heuristic rules.

Future improvements may include:

Learning-to-rank re-ranking

Larger assessment coverage

Domain-specific embedding fine-tuning

Author
Vedang Rajoriya
Final-year B.Tech student | AI / ML Enthusiast

Final Note
This project emphasizes clarity, robustness, and explainability, aligning with real-world SHL assessment recommendation use cases.