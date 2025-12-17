import pandas as pd
import requests
import time

API_URL = "http://localhost:8000/recommend"
DATASET_PATH = "data/Gen_AI Dataset.xlsx"
OUTPUT_PATH = "eval/test_predictions.csv"
TIMEOUT = 30


def find_column(columns, keywords):
    for col in columns:
        col_l = col.lower()
        for kw in keywords:
            if kw in col_l:
                return col
    return None


def generate_predictions():
    print("📘 Loading test dataset...")
    xls = pd.ExcelFile(DATASET_PATH)

    # Test data is usually the 2nd sheet
    test_df = pd.read_excel(xls, sheet_name=1)

    print("📄 Columns found in test sheet:")
    print(list(test_df.columns))

    query_col = find_column(
        test_df.columns,
        ["query", "job", "description", "requirement", "input"]
    )

    if not query_col:
        raise Exception("❌ Could not detect query column in test sheet")

    print(f"✅ Using query column: {query_col}")
    print("-" * 60)

    rows = []

    for idx, row in test_df.iterrows():
        query = str(row[query_col]).strip()
        if not query:
            continue

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
            continue

        recs = data.get("recommended_assessments", [])

        for r in recs:
            rows.append({
                "Query": query,
                "Assessment_url": r["url"]
            })

        print(f"[{idx+1}] Generated {len(recs)} recommendations")

        # small delay to be safe
        time.sleep(0.1)

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_PATH, index=False)

    print("\n✅ Test predictions saved to:", OUTPUT_PATH)
    print("📊 Total rows:", len(out_df))


if __name__ == "__main__":
    generate_predictions()
