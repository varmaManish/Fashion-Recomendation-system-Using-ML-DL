import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Device selection
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load pretrained model ONCE
_base_model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
_model = nn.Sequential(*list(_base_model.children())[:-1])
_model.eval()
_model.to(DEVICE)

# Image preprocessing pipeline
_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def extract_feature(image: Image.Image) -> np.ndarray:
    """
    Converts a PIL image into a normalized feature vector.
    """

    if image.mode != "RGB":
        image = image.convert("RGB")

    tensor = _transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        features = _model(tensor)

    # Flatten and normalize
    vector = features.squeeze().cpu().numpy()
    vector = vector / np.linalg.norm(vector)

    return vector
