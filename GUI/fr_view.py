import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
from PIL import Image, ImageTk

from face_recognition.recognition import recognize_face

def create_fr_view(parent_root):
    root = tk.Toplevel(parent_root)
    root.geometry("1000x600")

    root.config(bg="white")

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    selected_image_path = tk.StringVar()

    # # LEWA STRONA
    # ref_frame = tk.Frame(main_frame, bg="white")
    # ref_frame.pack(side="left", padx=30, pady=30, fill="y")
    #
    # ref_inner = tk.Frame(ref_frame, bg="white")
    # ref_inner.pack()
    #
    # ref_label = tk.Label(ref_inner, text="Reference", font=("Inter", 20, "bold"), bg="white")
    # ref_label.pack(pady=20)
    #
    # ref_btn_frame = tk.Frame(ref_inner, bg="white", bd=4, relief="solid", width=350, height=400)
    # ref_btn_frame.pack()
    # ref_btn_frame.pack_propagate(False)
    #
    # ref_btn_inner = tk.Frame(ref_btn_frame, bg="white")
    # ref_btn_inner.place(relx=0.5, rely=0.5, anchor="center")
    #
    # ref_btn = tk.Button(ref_btn_inner, text="Add Reference", bg="#6a4cbb", fg="white",
    #                                  font=("Inter", 16, "bold"))
    # ref_btn.pack()

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

    # camera_label = tk.Label(rec_btn_frame, bg="black")
    #
    # cap = None
    #
    #
    # def update_camera_frame():
    #     ret, frame = cap.read()
    #     if ret:
    #         frame = cv2.resize(frame, (640, 360))
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         img = Image.fromarray(frame)
    #         imgtk = ImageTk.PhotoImage(image=img)
    #         camera_label.imgtk = imgtk
    #         camera_label.config(image=imgtk)
    #     camera_label.after(10, update_camera_frame)
    #
    #
    # def start_camera():
    #     nonlocal cap
    #     cap = cv2.VideoCapture(0)
    #     if not cap.isOpened():
    #         tk.messagebox.showerror("Error", "Could not open camera.")
    #         return
    #     rec_btn_inner.place_forget()  # Ukryj przyciski
    #     camera_label.place(relx=0.5, rely=0.5, anchor="center", width=640, height=360)  # Pokaż kamerę
    #     update_camera_frame()
    #
    #
    # camera_btn.config(command=start_camera)

    # PRAWA STRONA
    start_frame = tk.Frame(main_frame, bg="white")
    start_frame.pack(side="left", padx=30, pady=30)

    # Funkcja realizujaca rozpoznawanie twarzy
    def recognize_selected_image():
        if not selected_image_path.get():
            messagebox.showwarning("Warning", "Please select an image first.")
            return
        try:
            match, score = recognize_face(selected_image_path.get())
            messagebox.showinfo("Result", f"Best match: {match} (score: {score:.3f})")
        except Exception as e:
            messagebox.showerror("Error", f"Recognition failed:\n{e}")


    start_btn = tk.Button(start_frame, text="Start", bg="#6a4cbb", fg="white", font=("Inter", 16, "bold"), command=recognize_selected_image)
    start_btn.pack(anchor="center")


    # Przycisk powrotu do MainView
    def go_back():
        root.destroy()  # Zamykamy ten widok
        parent_root.deiconify()  # Pokazujemy z powrotem MainView

    back_button = tk.Button(root, text="Back", font=("Inter", 16, "bold"),
                            bg="#6a4cbb", fg="white", command=go_back)
    back_button.pack(pady=10)

    def on_close():
        # if cap:
        #     cap.release()
        parent_root.quit()
        parent_root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    create_fr_view(root)
    root.mainloop()
