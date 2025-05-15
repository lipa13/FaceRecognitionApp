import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import shutil
from fr_view import create_fr_view

from face_recognition.save_reference import save_reference

def create_main_view():
    root = tk.Tk()
    root.title("MainView")

    root.geometry("1000x600")

    frame = tk.Frame(root)
    frame.pack(expand=True)

    label = tk.Label(frame, text="Face Recognition App", font=("Inter", 32, "bold"))
    label.pack(pady=(0, 60))

    def open_fr_view():
        root.withdraw()
        create_fr_view(root)

    face_rec_btn = tk.Button(frame, text="Start face recognition", bg="#6a4cbb", fg="white", font=("Inter", 16, "bold"),
                             width=30, command=open_fr_view)
    face_rec_btn.pack(pady=(0, 30))


    def add_reference():
        filepath = filedialog.askopenfilename(title="Choose a reference image",
                                              filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if filepath:
            # Ask for the person's name
            person_name = simpledialog.askstring("Name", "Enter the person's name:")
            if person_name:
                try:
                    save_reference(filepath, person_name)
                    messagebox.showinfo("Success", f"Image added and embedding saved for '{person_name}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add image:\n{e}")
            else:
                messagebox.showwarning("Cancelled", "You must enter a name.")


    add_ref_btn = tk.Button(frame, text="Add new reference image", bg="#6a4cbb", fg="white", font=("Inter", 16, "bold"),
                            width=30, command=add_reference)
    add_ref_btn.pack()

    root.mainloop()

if __name__ == "__main__":
    create_main_view()
