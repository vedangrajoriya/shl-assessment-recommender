import pandas as pd
import requests
import time

API_URL = "http://localhost:8000/recommend"
DATASET_PATH = "data/Gen_AI Dataset.xlsx"
TIMEOUT = 30


def find_column(columns, keywords):
    """
    Automatically find a column whose name contains
    any of the given keywords.
    """
    for col in columns:
        col_l = col.lower()
        for kw in keywords:
            if kw in col_l:
                return col
    return None


def recall_at_10():
    print("📘 Loading training dataset...")
    train_df = pd.read_excel(DATASET_PATH, sheet_name=0)

    print("📄 Columns found:")
    print(list(train_df.columns))

    # Auto-detect columns
    query_col = find_column(
        train_df.columns,
        ["query", "job", "description", "requirement", "input"]
    )
    url_col = find_column(
        train_df.columns,
        ["url", "assessment", "answer", "correct"]
    )

    if not query_col or not url_col:
        raise Exception("❌ Could not detect query or answer column automatically")

    print(f"✅ Using query column: {query_col}")
    print(f"✅ Using answer column: {url_col}")
    print("-" * 60)

    hits = []
    total = 0

    for idx, row in train_df.iterrows():
        query = str(row[query_col]).strip()
        true_url = str(row[url_col]).strip()

        if not query or not true_url:
            continue

        total += 1

        try:
            resp = requests.post(
                API_URL,
                json={"query": query},
                timeout=TIMEOUT
            )
        except Exception as e:
            print(f"⚠️ Request failed for query {idx+1}: {e}")
            continue

        if resp.status_code != 200:
            print(f"⚠️ API error {resp.status_code} for query {idx+1}")
            continue

        try:
            data = resp.json()
        except Exception:
            print(f"⚠️ Non-JSON response for query {idx+1}")
            print(resp.text[:200])
            continue

        if "recommended_assessments" not in data:
            print(f"⚠️ Missing key in response for query {idx+1}")
            continue

        top_urls = [
            r["url"]
            for r in data["recommended_assessments"][:10]
            if "url" in r
        ]

        hit = 1 if true_url in top_urls else 0
        hits.append(hit)

        status = "HIT" if hit else "MISS"
        print(f"[{idx+1}] {status} → {query[:70]}")

        # Small delay to avoid overloading API
        time.sleep(0.1)

    if not hits:
        print("\n❌ No valid queries evaluated")
        return

    recall = sum(hits) / len(hits)

    print("\n" + "=" * 60)
    print(f"🎯 Total evaluated queries : {len(hits)}")
    print(f"🎯 Mean Recall@10         : {round(recall, 3)}")
    print("=" * 60)


if __name__ == "__main__":
    recall_at_10()
