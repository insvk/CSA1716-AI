import argparse
from pathlib import Path

import cv2
import numpy as np

# This is face recognition, not merely face detection.
# Two reference images can be compared using OpenCV embeddings (LBPH).


def load_labeled_images(directory):
    directory = Path(directory)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = []
    labels = []
    names = []

    for label, image_path in enumerate(sorted(directory.glob("*.*")), start=1):
        image = cv2.imread(str(image_path))
        if image is None:
            continue
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detections = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(detections) == 0:
            continue

        x, y, w, h = max(detections, key=lambda box: box[2] * box[3])
        faces.append(cv2.resize(gray[y:y+h, x:x+w], (200, 200)))
        labels.append(label)
        names.append(image_path.stem)

    if not faces:
        raise ValueError("No labeled faces found. Place training face images in the supplied directory.")

    recognizer.train(faces, np.array(labels, dtype=np.int32))
    return recognizer, face_cascade, names


def recognize(image_path, directory):
    recognizer, cascade, names = load_labeled_images(directory)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detections = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in detections:
        face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
        label, confidence = recognizer.predict(face)
        name = names[label - 1] if 0 < label <= len(names) else "Unknown"
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(image, f"{name} ({confidence:.1f})", (x, y-8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    output_path = Path(__file__).resolve().parent / "recognized_faces.jpg"
    cv2.imwrite(str(output_path), image)
    print(f"Recognized {len(detections)} face(s). Output saved at: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recognize faces using OpenCV LBPH")
    parser.add_argument("--image", required=True, help="Image containing faces to recognize")
    parser.add_argument("--directory", required=True, help="Directory containing labeled training-face images")
    args = parser.parse_args()
    recognize(args.image, args.directory)
