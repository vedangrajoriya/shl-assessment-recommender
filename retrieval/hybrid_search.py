import numpy as np
import pandas as pd
import pickle
import re
from sentence_transformers import SentenceTransformer

CATALOG_PATH = "catalog/catalogue.csv"
EMB_PATH = "retrieval/embeddings.npy"
BM25_PATH = "retrieval/bm25.pkl"

def tokenize(text):
    return re.findall(r"\w+", text.lower())

class HybridSearch:
    def __init__(self):
        self.df = pd.read_csv(CATALOG_PATH)
        self.embeddings = np.load(EMB_PATH)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(BM25_PATH, "rb") as f:
            self.bm25 = pickle.load(f)

    def search(self, query, top_k=10, alpha=0.65):
        # Embedding score
        q_emb = self.model.encode([query], normalize_embeddings=True)[0]
        emb_scores = np.dot(self.embeddings, q_emb)

        # BM25 score
        tokens = tokenize(query)
        bm25_scores = self.bm25.get_scores(tokens)

        # Normalize scores
        emb_scores = (emb_scores - emb_scores.min()) / (emb_scores.max() - emb_scores.min() + 1e-8)
        bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-8)

        # Hybrid score
        scores = alpha * emb_scores + (1 - alpha) * bm25_scores

        top_idx = np.argsort(scores)[::-1][:top_k]

        results = self.df.iloc[top_idx].copy()
        results["score"] = scores[top_idx]

        return results

if __name__ == "__main__":
    hs = HybridSearch()
    res = hs.search("Need a SQL developer with good reasoning skills")
    print(res[["name", "score"]])
