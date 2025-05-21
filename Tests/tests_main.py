import os
import sys
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from face_recognition.recognition import recognize_face

def is_image_file(filename):
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    return filename.lower().endswith(image_extensions)


def recognize(image_path):
    try:
        match, score = recognize_face(image_path)
        return match, score
    except Exception as e:
        return f"Recognition failed: {e}", None



def run_tests(root_folder):
    for item in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, item)
        if os.path.isdir(subfolder_path):
            with open(f"Tests/{item}.csv", mode='w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=";")
                writer.writerow([item])  # Write folder name as section header
                
                print(f"Folder: {item}")
                n = 1
                for filename in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, filename)
                    if os.path.isfile(file_path) and is_image_file(filename):
                        match, score = recognize(file_path)
                        if score is not None:
                            writer.writerow([n, f"{score:.3f}", match])
                        else:
                            writer.writerow([n, "ERROR", match])
                        n += 1

                writer.writerow([])  # Empty line between folders


if __name__ == "__main__":
    #run_tests("Tests")
    pass
