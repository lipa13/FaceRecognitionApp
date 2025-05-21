import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import tempfile
import os

from face_recognition.recognition import recognize_face

def create_fr_view(parent_root):
    root = tk.Toplevel(parent_root)
    root.title("Face Recognition View")
    root.geometry("1000x600")

    root.config(bg="white")

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    selected_image_path = tk.StringVar()

    # LEWA STRONA
    rec_frame = tk.Frame(main_frame, bg="white")
    rec_frame.pack(side="left", padx=30, pady=30, fill="y")

    rec_inner = tk.Frame(rec_frame, bg="white")
    rec_inner.pack()

    rec_label = tk.Label(rec_inner, text="RECOGNIZE!", font=("Inter", 20, "bold"), bg="white")
    rec_label.pack(pady=20)

    rec_btn_frame = tk.Frame(rec_inner, bg="white", bd=4, relief="solid", width=640, height=360)
    rec_btn_frame.pack()
    rec_btn_frame.pack_propagate(False)

    rec_btn_inner = tk.Frame(rec_btn_frame, bg="white")
    rec_btn_inner.place(relx=0.5, rely=0.5, anchor="center")

    image_label = tk.Label(rec_btn_frame, bg="black")


    def load_image():
        filepath = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )

        if filepath:
            try:
                selected_image_path.set(filepath)
                img = Image.open(filepath)
                img = img.resize((640, 360))
                img_tk = ImageTk.PhotoImage(img)

                image_label.imgtk = img_tk
                image_label.config(image=img_tk)
                rec_btn_inner.place_forget()
                image_label.place(relx=0.5, rely=0.5, anchor="center", width=640, height=360)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image:\n{e}")


    local_st_btn = tk.Button(rec_btn_inner, text="Local Storage", bg="#6a4cbb", fg="white",
                             font=("Inter", 16, "bold"), command=load_image)
    local_st_btn.pack(pady=5)

    camera_btn = tk.Button(rec_btn_inner, text="Camera", bg="#6a4cbb", fg="white",
                           font=("Inter", 16, "bold"))
    camera_btn.pack(pady=5)

    camera_label = tk.Label(rec_btn_frame, bg="black")
    cap = None
    camera_running = False
    last_frame = None

    def start_camera():
        nonlocal cap, camera_running
        rec_btn_inner.place_forget()
        camera_label.place(relx=0.5, rely=0.5, anchor="center", width=640, height=360)
        camera_running = True

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        def update_frame():
            ret, frame = cap.read()
            if ret and camera_running:
                nonlocal last_frame
                last_frame = frame.copy()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=img)

                camera_label.imgtk = img_tk
                camera_label.configure(image=img_tk)

            camera_label.after(30, update_frame)

        update_frame()


    camera_btn.config(command=start_camera)

    # PRAWA STRONA
    start_frame = tk.Frame(main_frame, bg="white")
    start_frame.pack(side="left", padx=30, pady=30)

    def recognize_selected_image():
        if selected_image_path.get():
            # try to recognize from file
            try:
                match, score = recognize_face(selected_image_path.get())
                if match == "Hat Detected":
                    messagebox.showinfo("Message", "Please, remove your hat before face recognition!")
                else:
                    messagebox.showinfo("Result", f"Best match: {match} (score: {score:.3f})")
            except Exception as e:
                messagebox.showerror("Error", f"Recognition failed:\n{e}")
        elif last_frame is not None:
            # try to recognize from camera frame
            try:
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    temp_filename = tmp.name
                    cv2.imwrite(temp_filename, last_frame)

                match, score = recognize_face(temp_filename)
                os.remove(temp_filename)

                if match == "Hat Detected":
                    messagebox.showinfo("Message", "Please, remove your hat before face recognition!")
                else:
                    messagebox.showinfo("Result", f"Best match: {match} (score: {score:.3f})")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Recognition from camera failed:\n{e}")
        else:
            messagebox.showwarning("Warning", "Please load an image or open the camera first.")


    start_btn = tk.Button(start_frame, text="Start", bg="#6a4cbb", fg="white", font=("Inter", 16, "bold"), command=recognize_selected_image)
    start_btn.pack(anchor="center")

    def reload_view():
        nonlocal cap, camera_running, last_frame
        if cap:
            camera_label.place_forget()
            camera_label.config(image="")
            camera_running = False
            last_frame = None
            cap.release()

        # Ukryj label z obrazem
        image_label.place_forget()
        image_label.config(image="")

        # Wyzeruj ścieżkę do pliku
        selected_image_path.set("")

        # Pokaż z powrotem przyciski wyboru
        rec_btn_inner.place(relx=0.5, rely=0.5, anchor="center")

    reload_btn = tk.Button(start_frame, text="Reload", bg="#6a4cbb", fg="white", font=("Inter", 16, "bold"), command=reload_view)
    reload_btn.pack(anchor="center", pady=(10, 0))


    def go_back():
        root.destroy()
        parent_root.deiconify()


    back_button = tk.Button(root, text="Back", font=("Inter", 16, "bold"),
                            bg="#6a4cbb", fg="white", command=go_back)
    back_button.pack(pady=10)


    def on_close():
        reload_view()
        parent_root.quit()
        parent_root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    create_fr_view(root)
    root.mainloop()
