from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd

from retrieval.hybrid_search import HybridSearch
from retrieval.balanced_search import needs_balance, balance_results
from api.models import RecommendResponse, Assessment

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0"
)

# Initialize search engine once
search_engine = HybridSearch()


@app.get("/health")
def health():
    return {"status": "healthy"}


class QueryInput(BaseModel):
    query: str


# -----------------------------
# Query expansion for better recall
# -----------------------------
IMPORTANT_KEYWORDS = [
    "sql", "python", "java", "developer", "data",
    "analysis", "analytics", "sales", "communication",
    "leadership", "manager", "content", "writing",
    "stakeholder", "collaboration"
]


def clean_and_expand_query(query: str) -> str:
    q = query.lower()
    found = [k for k in IMPORTANT_KEYWORDS if k in q]
    return query + " " + " ".join(found)


# -----------------------------
# Recommend endpoint
# -----------------------------
@app.post("/recommend", response_model=RecommendResponse)
def recommend(payload: QueryInput):
    # 1️⃣ Clean + expand query
    raw_query = payload.query.strip()
    query = clean_and_expand_query(raw_query)

    # 2️⃣ Hybrid search with larger candidate pool
    results = search_engine.search(query, top_k=25)

    # ✅ ALWAYS define final_df (prevents crashes)
    final_df = results.head(10)

    # 3️⃣ Apply balancing only if required
    if needs_balance(query):
        has_behavior = final_df["test_type"].astype(str).str.contains(
            "Personality", case=False
        ).any()

        if not has_behavior:
            balanced = balance_results(results)
            final_df = pd.DataFrame(balanced)

    # 4️⃣ Build response
    assessments = []

    for _, row in final_df.iterrows():
        assessments.append(
            Assessment(
                url=row["url"],
                name=row["name"],
                adaptive_support=row["adaptive_support"],
                description=row["description"],
                duration=int(row["duration"]),
                remote_support=row["remote_support"],
                test_type=row["test_type"]
                if isinstance(row["test_type"], list)
                else eval(row["test_type"])
            )
        )

    return RecommendResponse(
        recommended_assessments=assessments
    )
