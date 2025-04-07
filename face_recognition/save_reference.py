import cv2
import os
import pickle

from face_sdk_wrapper import FaceSDKWrapper

def save_reference(image_path, person_name, output_db="face_recognition/data/embeddings.pkl"):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not load image: {image_path}")
        return

    # Get embedding
    sdk = FaceSDKWrapper()
    embedding = sdk.get_face_embedding(image)

    if embedding is None:
        print("No face found in the image.")
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_db), exist_ok=True)

    # Load existing database or create new
    if os.path.exists(output_db):
        with open(output_db, "rb") as f:
            db = pickle.load(f)
    else:
        db = {}

    # Save new reference
    #db[person_name] = embedding

    # Save or append new embedding
    # if person_name in db:
    #     db[person_name].append(embedding)
    # else:
    #     db[person_name] = [embedding]

    # with open(output_db, "wb") as f:
    #     pickle.dump(db, f)

    # Store embedding
    if person_name in db:
        # Convert existing numpy array to list if needed
        if isinstance(db[person_name], list):
            db[person_name].append(embedding)
        else:
            db[person_name] = [db[person_name], embedding]
    else:
        db[person_name] = [embedding]
    
    # Save updated database
    with open(output_db, "wb") as f:
        pickle.dump(db, f)


    print(f"[INFO] Saved embedding for '{person_name}' into '{output_db}'.")


if __name__ == "__main__":
    image_path = input("Path to reference image: ")
    name = input("Person's name: ")
    save_reference(image_path, name)