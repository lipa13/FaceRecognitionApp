import cv2
import os
import pickle
import numpy as np
from face_sdk_wrapper import FaceSDKWrapper

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Recognize face from image
def recognize_face(image_path, db_path="face_recognition/data/embeddings.pkl", threshold=0.6):
    if not os.path.exists(db_path):
        print(f"Embedding database not found at '{db_path}'")
        return

    # Load reference embeddings
    with open(db_path, "rb") as f:
        db = pickle.load(f)

    # Load input image
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Could not load image: {image_path}")
        return None

    # Extract embedding
    sdk = FaceSDKWrapper()
    embedding = sdk.get_face_embedding(image)
    if embedding is None:
        print("[ERROR] No face detected in the input image.")
        return None

    # Compare with database
    best_match = "Unknown"
    best_score = -1

    for name, ref_embedding in db.items():
        score = cosine_similarity(embedding, ref_embedding)
        print(f"[INFO] Similarity with {name}: {score:.3f}")
        if score > best_score:
            best_score = score
            best_match = name

    if best_score < threshold:
        best_match = "Unknown"

    print(f"\n[RESULT] Best match: {best_match} (score: {best_score:.3f})")
    return best_match

if __name__ == "__main__":
    image_path = input("Path to image for recognition: ")
    recognize_face(image_path)