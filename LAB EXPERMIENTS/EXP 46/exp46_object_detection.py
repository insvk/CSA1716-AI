import torch
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights

# Load Pre-trained Machine Learning Model (Faster R-CNN)
print("Loading pre-trained model...")
weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn(weights=weights)
model.eval() # Set to evaluation mode

# Create a dummy image tensor (C, H, W) to simulate an input image
# Values normalized between 0 and 1
dummy_image = torch.rand(3, 300, 400)

print("Performing Object Detection...")
with torch.no_grad():
    predictions = model([dummy_image])

# Output results
num_objects = len(predictions[0]['boxes'])
print(f"Detected {num_objects} potential objects in the image.")
if num_objects > 0:
    print("Top Bounding Box (xmin, ymin, xmax, ymax):", predictions[0]['boxes'][0].numpy())
    print("Top Confidence Score:", predictions[0]['scores'][0].numpy())
