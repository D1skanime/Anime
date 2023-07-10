import tkinter as tk
from tkinter import messagebox
import glob
import os


def delete_images(folder_path):
    print("\nAktueller Ordner:", folder_path)
    image_extensions = ["jpg", "png", "gif", "bif", "nfo"]
    image_files = []
    for extension in image_extensions:
        image_files.extend(glob.glob(folder_path + "/*." + extension))

    if not image_files:
        messagebox.showinfo("Keine Dateien gefunden", "Es wurden keine JPG- und PNG-Dateien gefunden.")
        return

    root = tk.Tk()
    root.title("Bilder löschen")
    root.geometry("600x500")

    label = tk.Label(root, text="Gefundene Dateien:")
    label.pack(pady=10)

    checkbox_frame = tk.Frame(root)
    checkbox_frame.pack(pady=10)

    checkboxes = []
    selected_extensions = []

    def toggle_extension(extension):
        if extension in selected_extensions:
            selected_extensions.remove(extension)
        else:
            selected_extensions.append(extension)

    for extension in image_extensions:
        if any(file.endswith("." + extension) for file in image_files):
            checkbox = tk.Checkbutton(checkbox_frame, text=extension, command=lambda ext=extension: toggle_extension(ext))
            checkbox.pack(side=tk.LEFT)
            checkboxes.append(checkbox)

    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    listbox.pack(fill=tk.BOTH, expand=True)
    for file in image_files:
        listbox.insert(tk.END, file)

   
    # Funktion zum löschen und anzeigen
    def delete_selected():
        selected_indices = listbox.curselection()
        selected_files = [image_files[index] for index in selected_indices]
        
        if selected_files or selected_extensions:
            if selected_extensions:
                for file in image_files:
                    file_extension = os.path.splitext(file)[1][1:].lower()
                    if file_extension in selected_extensions:
                        try:
                            os.remove(file)
                            listbox.delete(listbox.get(0, tk.END).index(file))
                        except OSError as e:
                            messagebox.showerror("Fehler beim Löschen", f"Fehler beim Löschen der Datei {file}: {e.strerror}")
            elif selected_files:
                for file in selected_files:
                    try:
                        os.remove(file)
                        listbox.delete(listbox.get(0, tk.END).index(file))
                    except OSError as e:
                        messagebox.showerror("Fehler beim Löschen", f"Fehler beim Löschen der Datei {file}: {e.strerror}")
        
        root.destroy()

    delete_button = tk.Button(root, text="Ausgewählte löschen", command=delete_selected)
    delete_button.pack(pady=10)

    root.mainloop()
    return
