import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# --------------------------------------------------
# Resolve paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "backend" / "data"

FEATURES_PATH = DATA_DIR / "fashion_features.npy"
METADATA_PATH = DATA_DIR / "fashion_metadata.csv"

# --------------------------------------------------
# Load data ONCE (module-level cache)
# --------------------------------------------------
_features = np.load(FEATURES_PATH)
_metadata = pd.read_csv(METADATA_PATH).reset_index(drop=True)

# --------------------------------------------------
# Defensive sanity check
# --------------------------------------------------
if _features.shape[0] != len(_metadata):
    raise RuntimeError(
        f"Data mismatch: {_features.shape[0]} features "
        f"vs {len(_metadata)} metadata rows"
    )

# --------------------------------------------------
# Public API
# --------------------------------------------------
def recommend_similar(query_vector: np.ndarray, top_k: int = 8):
    """
    Given a query feature vector, return top_k visually similar products.
    """

    if query_vector.ndim != 1:
        raise ValueError("query_vector must be a 1D array")

    # Normalize query vector
    query_vector = query_vector / np.linalg.norm(query_vector)
    query_vector = query_vector.reshape(1, -1)

    # Compute cosine similarity
    similarities = cosine_similarity(query_vector, _features)[0]

    # Get top-k indices
    # Sort by similarity (descending)
    sorted_indices = np.argsort(similarities)[::-1]
   # Remove self-match (first index)
    top_indices = sorted_indices[1:top_k+1]


    results = []

    for idx in top_indices:
        row = _metadata.iloc[idx]
        filename = row["filename"]

        results.append({
            "id": int(idx),
            "name": filename.replace(".jpg", ""),
            "image": f"/static/images/{filename}",
            "similarity": round(float(similarities[idx]), 4)
        })

    return results