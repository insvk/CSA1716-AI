import cv2
import numpy as np

# Create a synthetic image for segmentation
img = np.zeros((200, 200, 3), dtype=np.uint8)
img[:, :100] = [255, 0, 0]   # Blue left
img[:, 100:] = [0, 255, 0]   # Green right
cv2.circle(img, (100, 100), 50, (0, 0, 255), -1) # Red circle in center

# Reshape image for k-means processing
pixel_values = img.reshape((-1, 3))
pixel_values = np.float32(pixel_values)

# Define criteria and apply K-Means for image segmentation
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
k = 3 # Segment into 3 colors
_, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Reconstruct segmented image
centers = np.uint8(centers)
segmented_data = centers[labels.flatten()]
segmented_image = segmented_data.reshape((img.shape))

cv2.imwrite("segmented_output.jpg", segmented_image)
print("Image segmentation complete. Output saved as 'segmented_output.jpg'.")
