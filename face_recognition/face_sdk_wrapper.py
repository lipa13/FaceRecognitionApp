import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

sys.path.insert(0, os.path.abspath("face_sdk"))

import yaml
import cv2
import numpy as np
from face_sdk.core.model_loader.face_detection.FaceDetModelLoader import FaceDetModelLoader
from face_sdk.core.model_handler.face_detection.FaceDetModelHandler import FaceDetModelHandler
from face_sdk.core.model_loader.face_alignment.FaceAlignModelLoader import FaceAlignModelLoader
from face_sdk.core.model_handler.face_alignment.FaceAlignModelHandler import FaceAlignModelHandler
from face_sdk.core.image_cropper.arcface_cropper.FaceRecImageCropper import FaceRecImageCropper
from face_sdk.core.model_loader.face_recognition.FaceRecModelLoader import FaceRecModelLoader
from face_sdk.core.model_handler.face_recognition.FaceRecModelHandler import FaceRecModelHandler


class FaceSDKWrapper:
    def __init__(self, config_path="face_sdk/config/model_conf.yaml", device="cpu"):
        # Load config
        with open(config_path, 'r') as f:
            self.cfg = yaml.safe_load(f)

        self.device = device
        self.scene = 'non-mask'  # You can expose this as an init parameter if needed
        model_path = "face_sdk/models"

        # Load face detection model
        det_model_name = self.cfg[self.scene]['face_detection']
        det_loader = FaceDetModelLoader(model_path, 'face_detection', det_model_name)
        det_model, det_cfg = det_loader.load_model()
        self.det_handler = FaceDetModelHandler(det_model, device, det_cfg)

        # Load face alignment model
        align_model_name = self.cfg[self.scene]['face_alignment']
        align_loader = FaceAlignModelLoader(model_path, 'face_alignment', align_model_name)
        align_model, align_cfg = align_loader.load_model()
        self.align_handler = FaceAlignModelHandler(align_model, device, align_cfg)

        # Load face recognition model
        rec_model_name = self.cfg[self.scene]['face_recognition']
        rec_loader = FaceRecModelLoader(model_path, 'face_recognition', rec_model_name)
        rec_model, rec_cfg = rec_loader.load_model()
        self.rec_handler = FaceRecModelHandler(rec_model, device, rec_cfg)

        # Face cropper
        self.cropper = FaceRecImageCropper()

    def get_face_embedding(self, image):
        """Returns the embedding of the first detected face in the image."""
        dets = self.det_handler.inference_on_image(image)
        if dets is None or len(dets) == 0:
            print("No face detected.")
            return None

        det = dets[0]
        landmarks = self.align_handler.inference_on_image(image, det)
        landmarks_list = []
        for (x, y) in landmarks.astype(np.int32):
            landmarks_list.extend((x, y))
        cropped = self.cropper.crop_image_by_mat(image, landmarks_list)
        embedding = self.rec_handler.inference_on_image(cropped)
        return embedding


    def draw_detections(self, image):
        image_copy = image.copy()
        dets = self.det_handler.inference_on_image(image)
        for det in dets:
            x1, y1, x2, y2, score = map(int, det)
            cv2.rectangle(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return image_copy


    def get_cropped_face(self, image):
        dets = self.det_handler.inference_on_image(image)
        if dets is None or len(dets) == 0:
            return None
        det = dets[0]
        landmarks = self.align_handler.inference_on_image(image, det)
        landmarks_list = [coord for (x, y) in landmarks.astype(np.int32) for coord in (x, y)]
        cropped = self.cropper.crop_image_by_mat(image, landmarks_list)
        return cropped


# if __name__ == "__main__":
#     img_path = input("Enter path to test image: ")
#     img = cv2.imread(img_path)
#     sdk = FaceSDKWrapper()
#     emb = sdk.get_face_embedding(img)
#     if emb is not None:
#         print("Embedding extracted successfully!")
#         print(emb[:5], "...")
#     else:
#         print("No face found.")

if __name__ == "__main__":
    img_path = input("Enter path to test image: ")
    image = cv2.imread(img_path)
    sdk = FaceSDKWrapper()

    # Generate visualizations
    detection_img = sdk.draw_detections(image)
    cropped_face = sdk.get_cropped_face(image)

    # Save outputs
    out_dir = "face_recognition/output"
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, "detected_faces.jpg"), detection_img)
    if cropped_face is not None:
        cv2.imwrite(os.path.join(out_dir, "cropped_face.jpg"), cropped_face)

    # Also try embedding
    emb = sdk.get_face_embedding(image)
    if emb is not None:
        print("Embedding extracted successfully!")
        print(emb[:5], "...")
    else:
        print("No face found.")