import pandas as pd
from rank_bm25 import BM25Okapi
import pickle
import re

CATALOG_PATH = "catalog/catalogue.csv"
OUTPUT_BM25 = "retrieval/bm25.pkl"

def tokenize(text):
    return re.findall(r"\w+", text.lower())

def main():
    df = pd.read_csv(CATALOG_PATH)

    corpus = (df["name"] + " " + df["description"]).tolist()
    tokenized = [tokenize(text) for text in corpus]

    bm25 = BM25Okapi(tokenized)

    with open(OUTPUT_BM25, "wb") as f:
        pickle.dump(bm25, f)

    print("✅ BM25 index saved to:", OUTPUT_BM25)

if __name__ == "__main__":
    main()
