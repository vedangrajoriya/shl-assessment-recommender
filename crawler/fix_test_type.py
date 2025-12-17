import pandas as pd
import ast

CATALOG_PATH = "catalog/catalogue.csv"

BEHAVIOR_KEYWORDS = [
    "personality", "behavior", "behaviour",
    "communication", "leadership", "sales",
    "management", "team", "collaboration"
]

def fix_types():
    df = pd.read_csv(CATALOG_PATH)

    new_types = []

    for _, row in df.iterrows():
        name = row["name"].lower()
        url = row["url"].lower()

        is_behavior = any(k in name or k in url for k in BEHAVIOR_KEYWORDS)

        if is_behavior:
            new_types.append(["Personality & Behavior"])
        else:
            new_types.append(["Knowledge & Skills"])

    df["test_type"] = new_types
    df.to_csv(CATALOG_PATH, index=False)

    print("✅ test_type corrected in catalogue.csv")

if __name__ == "__main__":
    fix_types()
