import numpy as np
import torch
from torchvision.models.detection import (
    FasterRCNN_ResNet50_FPN_Weights,
    fasterrcnn_resnet50_fpn,
)

weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn(weights=weights)
model.eval()
preprocess = weights.transforms()

# Generate a reproducible image tensor and run detection.
generator = torch.Generator().manual_seed(42)
dummy_image = torch.rand((3, 300, 400), generator=generator)
input_tensor = preprocess(dummy_image)

with torch.inference_mode():
    prediction = model([input_tensor])[0]

confidence_threshold = 0.5
keep = prediction["scores"] >= confidence_threshold
boxes = prediction["boxes"][keep].cpu()
scores = prediction["scores"][keep].cpu()
labels = prediction["labels"][keep].cpu()
categories = weights.meta["categories"]

print(f"Detected {len(boxes)} objects above confidence {confidence_threshold:.2f}.")
for box, score, label in zip(boxes, scores, labels):
    print(
        f"{categories[label.item()]}: "
        f"confidence={score.item():.3f}, box={np.round(box.numpy(), 1).tolist()}"
    )
