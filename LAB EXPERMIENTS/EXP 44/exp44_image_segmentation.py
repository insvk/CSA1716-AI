from pathlib import Path

import cv2
import numpy as np

# Create a reproducible synthetic image.
image = np.zeros((200, 200, 3), dtype=np.uint8)
image[:, :100] = [255, 0, 0]
image[:, 100:] = [0, 255, 0]
cv2.circle(image, (100, 100), 50, (0, 0, 255), -1)

pixels = np.float32(image.reshape(-1, 3))
criteria = (
    cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
    100,
    0.2,
)

_, labels, centers = cv2.kmeans(
    pixels,
    3,
    None,
    criteria,
    10,
    cv2.KMEANS_PP_CENTERS,
)

segmented = np.uint8(centers)[labels.flatten()].reshape(image.shape)
output_path = Path(__file__).resolve().parent / "segmented_output.jpg"
cv2.imwrite(str(output_path), segmented)
print(f"Image segmentation complete. Output saved at: {output_path}")
