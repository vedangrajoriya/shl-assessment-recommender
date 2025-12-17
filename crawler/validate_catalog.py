import pandas as pd
import ast

CATALOG_PATH = "catalog/catalogue.csv"

df = pd.read_csv(CATALOG_PATH)

print("🔍 Basic info")
print(df.info())
print("\n📊 Row count:", len(df))

# Required columns
required_cols = {
    "name",
    "url",
    "description",
    "duration",
    "adaptive_support",
    "remote_support",
    "test_type"
}

missing = required_cols - set(df.columns)
if missing:
    raise Exception(f"❌ Missing columns: {missing}")

# Empty checks
if df["name"].isna().any() or df["url"].isna().any():
    raise Exception("❌ name or url has missing values")

# Yes/No validation
for col in ["adaptive_support", "remote_support"]:
    bad = df[~df[col].isin(["Yes", "No"])]
    if not bad.empty:
        raise Exception(f"❌ Invalid values in {col}")

# Duration check
if not pd.api.types.is_integer_dtype(df["duration"]):
    print("⚠️ duration is not integer, attempting fix...")
    df["duration"] = df["duration"].astype(int)

# test_type validation
def check_test_type(x):
    try:
        v = ast.literal_eval(x) if isinstance(x, str) else x
        return isinstance(v, list) and len(v) > 0
    except:
        return False

if not df["test_type"].apply(check_test_type).all():
    raise Exception("❌ test_type column is malformed")

print("\n✅ Catalog validation PASSED")
