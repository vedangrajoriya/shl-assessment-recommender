import pandas as pd
import re
import os

DATASET_PATH = "data/Gen_AI Dataset.xlsx"
OUTPUT_PATH = "catalog/catalogue.csv"

def infer_test_type(url: str):
    u = url.lower()
    types = []
    if any(k in u for k in ["personality", "behavior", "behaviour"]):
        types.append("Personality & Behavior")
    if any(k in u for k in ["skill", "knowledge", "cognitive", "ability", "reasoning"]):
        types.append("Knowledge & Skills")
    if not types:
        types.append("Knowledge & Skills")
    return types

def infer_name_from_url(url: str):
    slug = url.rstrip("/").split("/")[-1]
    name = slug.replace("-", " ").replace("_", " ").title()
    return name

def build_catalog():
    print("📘 Reading Excel dataset...")
    xls = pd.ExcelFile(DATASET_PATH)

    all_urls = set()

    # Go through every sheet
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        print(f"🔍 Processing sheet: {sheet}")

        for col in df.columns:
            if "url" in col.lower():
                urls = df[col].dropna().astype(str).tolist()
                for u in urls:
                    if u.startswith("http"):
                        all_urls.add(u.strip())

    print(f"✅ Found {len(all_urls)} unique assessment URLs")

    if len(all_urls) == 0:
        raise Exception("❌ No URLs found in dataset")

    rows = []
    for url in sorted(all_urls):
        rows.append({
            "name": infer_name_from_url(url),
            "url": url,
            "description": "SHL assessment used for talent evaluation.",
            "duration": -1,  # unknown
            "adaptive_support": "Yes",  # safe default
            "remote_support": "Yes",    # safe default
            "test_type": infer_test_type(url)
        })

    catalog_df = pd.DataFrame(rows)

    os.makedirs("catalog", exist_ok=True)
    catalog_df.to_csv(OUTPUT_PATH, index=False)

    print("🎉 Catalogue built successfully!")
    print(f"📄 Saved to: {OUTPUT_PATH}")
    print(f"📊 Total assessments in catalog: {len(catalog_df)}")

if __name__ == "__main__":
    build_catalog()
