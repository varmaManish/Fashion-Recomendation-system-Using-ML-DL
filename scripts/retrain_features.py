import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
from tqdm import tqdm

import torch
import torch.nn as nn
from torchvision import models, transforms

# ---------------- CONFIG ----------------
IMAGE_DIR = Path("frontend/static/images")
METADATA_PATH = Path("backend/data/fashion_metadata.csv")
OUTPUT_FEATURES = Path("backend/data/fashion_features.npy")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# ----------------------------------------

# Load metadata
df = pd.read_csv(METADATA_PATH)

# Load model
base = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model = nn.Sequential(*list(base.children())[:-1])
model.eval().to(DEVICE)

# Transform (ImageNet standard)
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

features = []

print("🔁 Retraining embeddings...")

for _, row in tqdm(df.iterrows(), total=len(df)):
    img_path = IMAGE_DIR / row["filename"]

    if not img_path.exists():
        raise FileNotFoundError(f"Missing image: {img_path}")

    img = Image.open(img_path).convert("RGB")
    tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        feat = model(tensor).squeeze().cpu().numpy()

    # normalize
    feat = feat / np.linalg.norm(feat)
    features.append(feat)

features = np.array(features)

# Save
np.save(OUTPUT_FEATURES, features)

print("✅ DONE")
print("Features shape:", features.shape)
print("Saved to:", OUTPUT_FEATURES)
