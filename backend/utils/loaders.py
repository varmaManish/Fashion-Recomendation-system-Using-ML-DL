import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------
# Resolve base paths safely
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "backend" / "data"

FEATURES_PATH = DATA_DIR / "fashion_features.npy"
METADATA_PATH = DATA_DIR / "fashion_metadata.csv"

# --------------------------------------------------
# Load metadata
# --------------------------------------------------
def load_metadata():
    """
    Load product metadata CSV.
    """
    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"Metadata file not found at {METADATA_PATH}")

    df = pd.read_csv(METADATA_PATH)
    df = df.reset_index(drop=True)

    return df


# --------------------------------------------------
# Load features
# --------------------------------------------------
def load_features():
    """
    Load feature vectors (NumPy).
    """
    if not FEATURES_PATH.exists():
        raise FileNotFoundError(f"Features file not found at {FEATURES_PATH}")

    features = np.load(FEATURES_PATH)

    return features
