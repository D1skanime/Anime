import os
import re
import tkinter as tk

def create_gui(text_data, path):
    window = tk.Tk()

    def on_checkbox_click():
        selected_text = [text_data[i] for i, value in enumerate(checkbox_values) if value.get() == 1]
        if selected_text:
            gruppename = "-".join(selected_text)
            window.destroy()
            return gruppename

    checkbox_values = []
    for text in text_data:
        checkbox_value = tk.IntVar()
        checkbox_values.append(checkbox_value)
        checkbox = tk.Checkbutton(window, text=text, variable=checkbox_value)
        checkbox.pack()

    ok_button = tk.Button(window, text="OK", command=on_checkbox_click)
    ok_button.pack()

    window.mainloop()


# Finde den Gruppennamen für die Folge im Verzeichnis
def finde_groupname(path, SourceList, path_text):
    Videofiles = os.listdir(path)

    with open(path_text, 'r') as file:
        text_data = file.read().split('\n')
   

    for file in Videofiles:
        # Überprüfe, ob die Datei eine Videodatei ist
        if any(file.lower().endswith(ext) for ext in SourceList):
            # Extrahiere den Gruppennamen aus dem Dateinamen
            print("------------------------------------------")
            print("\n".join(Videofiles)) 
            print("\n""------------------------------------------")
            match = re.search(r"^\[(.*?)\]|(?<=-)[A-Za-z0-9_-]+(?=\.)", file)
            if match:
                Gruppename = match.group(0)
                return "-"+Gruppename
            else:
                create_gui(text_data, path_text)
                return "-"+Gruppename
