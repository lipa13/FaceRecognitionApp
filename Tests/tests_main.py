def is_image_file(filename):
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    return filename.lower().endswith(image_extensions)


def recognize(image_path):
    result = ""
    try:
        match, score = recognize_face(image_path)
        result += f"Best match = {match}, score = {score:.3f}"
    except Exception as e:
        result += f"Recognition failed:\n{e}"

    return result


def run_tests(root_folder):
    # Przeglądanie podfolderów w głównym katalogu
    for item in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, item)
        # Sprawdzamy czy dana ścieżka jest katalogiem
        if os.path.isdir(subfolder_path):
            print(f"\nFolder: {item}\n") # Print nazwy katalogu
            n = 1
            for filename in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, filename)
                if os.path.isfile(file_path) and is_image_file(filename):
                    print(f"\nTest {n}: {recognize(file_path)}")
                    n = n + 1
            print("\n")


if __name__ == "__main__":
    pass