import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os

CATALOG_PATH = "catalog/catalogue.csv"
OUTPUT_EMB = "retrieval/embeddings.npy"

def main():
    print("📄 Loading catalog...")
    df = pd.read_csv(CATALOG_PATH)

    texts = (df["name"] + ". " + df["description"]).tolist()

    print("🧠 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("⚙️ Generating embeddings...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    os.makedirs("retrieval", exist_ok=True)
    np.save(OUTPUT_EMB, embeddings)

    print("✅ Embeddings saved to:", OUTPUT_EMB)
    print("📊 Shape:", embeddings.shape)

if __name__ == "__main__":
    main()
