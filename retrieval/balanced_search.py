import numpy as np
from retrieval.hybrid_search import HybridSearch


BEHAVIOR_WORDS = [
    "collaboration", "communication", "team",
    "stakeholder", "leadership", "behavior", "personality"
]

TECH_WORDS = [
    "sql", "python", "java", "coding",
    "analysis", "developer", "technical", "data"
]

def needs_balance(query: str) -> bool:
    q = query.lower()
    has_beh = any(w in q for w in BEHAVIOR_WORDS)
    has_tech = any(w in q for w in TECH_WORDS)
    return has_beh and has_tech

def balance_results(df, top_k=10, min_behavioral=2):
    tech = df[df["test_type"].astype(str).str.contains("Knowledge")]
    beh = df[df["test_type"].astype(str).str.contains("Personality")]

    results = []

    # Add technical first
    for _, row in tech.iterrows():
        results.append(row)
        if len(results) >= top_k:
            break

    # Replace last items with behavioral to ensure mix
    if len(beh) >= min_behavioral:
        for i in range(min_behavioral):
            results[-(i+1)] = beh.iloc[i]

    return results[:top_k]

if __name__ == "__main__":
    hs = HybridSearch()
    query = "Need a SQL developer who can collaborate with stakeholders"
    df = hs.search(query, top_k=15)

    if needs_balance(query):
        balanced = balance_results(df)
        print("🔀 Balanced results:")
        for r in balanced:
            print(r["name"])
    else:
        print(df[["name", "score"]])
