import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from face_recognition.save_reference import save_reference

def is_image_file(filename):
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    return filename.lower().endswith(image_extensions)


def save_all_images_from_folder(folder_path, person_name):
    print(f"Saving references for: {person_name}")

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and is_image_file(filename):
            try:
                save_reference(file_path, person_name)
                print(f"Saved: {filename}")
            except Exception as e:
                print(f"Failed to save {filename}: {e}")


if __name__ == "__main__":
    #save_all_images_from_folder("Tests/images/BAZA/kuba_baza", "Kuba")
    pass
