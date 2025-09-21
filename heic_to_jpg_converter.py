
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_heif
import os

def convert_heic_to_jpg(heic_path, jpg_path):
    try:
        heif_file = pillow_heif.read_heif(heic_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(jpg_path, "JPEG")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert {os.path.basename(heic_path)}:\n{e}")
        return False

def select_files():
    files = filedialog.askopenfilenames(title="Select HEIC files", filetypes=[("HEIC files", "*.heic")])
    entry_files.delete(0, tk.END)
    entry_files.insert(0, ";".join(files))

def select_output_dir():
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    entry_output_dir.delete(0, tk.END)
    entry_output_dir.insert(0, output_dir)

def start_conversion():
    heic_files = entry_files.get().split(";")
    output_dir = entry_output_dir.get()

    if not heic_files or not output_dir:
        messagebox.showwarning("Warning", "Please select HEIC files and an output directory.")
        return

    for heic_file in heic_files:
        if heic_file:
            base_name = os.path.basename(heic_file)
            jpg_name = os.path.splitext(base_name)[0] + ".jpg"
            jpg_path = os.path.join(output_dir, jpg_name)
            convert_heic_to_jpg(heic_file, jpg_path)

    messagebox.showinfo("Success", "Conversion complete!")

# Create the main window
root = tk.Tk()
root.title("HEIC to JPG Converter")

# Create and pack the widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label_files = tk.Label(frame, text="HEIC Files:")
label_files.grid(row=0, column=0, sticky="w")

entry_files = tk.Entry(frame, width=50)
entry_files.grid(row=0, column=1, padx=5)

btn_select_files = tk.Button(frame, text="Select Files", command=select_files)
btn_select_files.grid(row=0, column=2)

label_output_dir = tk.Label(frame, text="Output Directory:")
label_output_dir.grid(row=1, column=0, sticky="w")

entry_output_dir = tk.Entry(frame, width=50)
entry_output_dir.grid(row=1, column=1, padx=5)

btn_select_output_dir = tk.Button(frame, text="Select Directory", command=select_output_dir)
btn_select_output_dir.grid(row=1, column=2)

btn_convert = tk.Button(root, text="Convert", command=start_conversion)
btn_convert.pack(pady=10)

root.mainloop()
