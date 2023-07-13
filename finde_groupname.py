import os
import re
import tkinter as tk

def create_gui(text_data):
    global result # <============ Mind this

    window = tk.Tk()
    result = None

    def on_checkbox_click():
        global result # <============ Mind this
        selected_text = [text_data[i] for i, value in enumerate(checkbox_values) if value.get() == 1]
        if selected_text:
            gruppename = "-".join(selected_text)
            window.destroy()
            result = gruppename

    checkbox_values = []

    for text in text_data:
        checkbox_value = tk.IntVar()
        checkbox_values.append(checkbox_value)
        checkbox = tk.Checkbutton(window, text=text, variable=checkbox_value)
        checkbox.pack()

    ok_button = tk.Button(window, text="OK", command=on_checkbox_click)
    ok_button.pack()

    window.mainloop()
    return result

def SaveGruppeName(Neuer_Gruppename_eintrag,path_text):
    Animetexteintragneu = open(path_text, "a")
    Animetexteintragneu.write("\n" + Neuer_Gruppename_eintrag)
    Animetexteintragneu.close()
    return


# Finde den Gruppennamen für die Folge im Verzeichnis
def finde_groupname(path, SourceList, path_text):
    Videofiles = os.listdir(path)
    text_data = []
    with open(path_text, 'r', encoding="cp1252") as file:
        text_data = [_.rstrip('\n') for _ in file]

   

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
                pattern = r"\b" + re.escape(Gruppename) + r"\b"
                if not re.search(pattern, ' '.join(text_data)):
                    SaveGruppeName(Gruppename ,path_text)
                    return "-"+Gruppename
                else:
                    return "-"+Gruppename
            else:
                Gruppename = create_gui(text_data)
                return "-"+Gruppename
