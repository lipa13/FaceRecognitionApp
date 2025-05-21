import cv2
import os
import pickle
import numpy as np
from face_recognition.face_sdk_wrapper import FaceSDKWrapper

from ultralytics import YOLO

# Load YOLOv8 model once (global, to avoid reloading every call)
yolo_model = YOLO("face_recognition/models/best.pt")  # or "yolov8s.pt" for slightly better accuracy

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Recognize face from image
def recognize_face(image_path, db_path="face_recognition/data/embeddings.pkl", threshold=0.6):
    print(yolo_model.names)
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

    ### --- Hat Detection Step ---
    results = yolo_model(image)[0]  # Get predictions
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = yolo_model.names[cls_id]

        if "cap" in label.lower() and conf > 0.6:
            print("[WARNING] Hat detected on the head. Please remove your hat before recognition.")
            return "Hat Detected", 0.0
    ### -------------------------

    # Extract embedding
    sdk = FaceSDKWrapper()
    embedding = sdk.get_face_embedding(image)
    if embedding is None:
        print("[ERROR] No face detected in the input image.")
        return None

    # Compare with database
    best_match = "Unknown"
    best_score = -1

    #for name, ref_embedding in db.items():
        #score = cosine_similarity(embedding, ref_embedding)
        #print(f"[INFO] Similarity with {name}: {score:.3f}")

        # if score > best_score:
        #     best_score = score
        #     best_match = name
    
    for name, embeddings_list in db.items():
        # Support both single and multiple embeddings (for backward compatibility)
        if not isinstance(embeddings_list, list):
            embeddings_list = [embeddings_list]

        # Compute similarity for each stored embedding
        # person_best = max(cosine_similarity(embedding, ref_emb) for ref_emb in embeddings_list)

        # print(f"[INFO] Max similarity with {name}: {person_best:.3f}")

        #print(f"\n[INFO] Similarities with {name}:")

        # Compute and print similarity for each embedding
        scores = []
        for i, ref_emb in enumerate(embeddings_list):
            score = cosine_similarity(embedding, ref_emb)
            scores.append(score)
            #print(f"    - Embedding {i+1}: {score:.3f}")

        person_best = max(scores)

        if person_best > best_score:
            best_score = person_best
            best_match = name

    if best_score < threshold:
        best_match = "Unknown"

    #print(f"\n[RESULT] Best match: {best_match} (score: {best_score:.3f})")
    return best_match, best_score

if __name__ == "__main__":
    image_path = input("Path to image for recognition: ")
    recognize_face(image_path)