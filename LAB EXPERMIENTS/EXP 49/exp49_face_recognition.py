import cv2
import numpy as np

# Note: Uses OpenCV's pre-trained Haar Cascade for Face Detection
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# Create a synthetic dummy image simulating a basic face-like structure
img = np.zeros((400, 400, 3), dtype=np.uint8)
# Background
img[:] = (200, 200, 200)
# Draw a face-like shape that Haar Cascade might trigger on (or load a real image)
# For real usage: img = cv2.imread('your_face_image.jpg')
cv2.circle(img, (200, 200), 100, (255, 220, 200), -1)

# Convert to grayscale (required for Haar Cascades)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Perform Face Detection
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

print(f"Face Recognition model executed.")
print(f"Detected {len(faces)} face(s) in the image array.")
cv2.imwrite("detected_faces.jpg", img)
