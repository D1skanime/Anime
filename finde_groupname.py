import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLineEdit

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
result = None

def on_checkbox_click():
    global result
    selected_text = [text_data[i] for i, value in enumerate(checkbox_values) if value.isChecked()]
    if selected_text:
        gruppename = "-".join(selected_text)
        window.close()
        result = gruppename
    else:
        new_groupname = new_group_input.text()
        if new_groupname:
            window.close()
            result = new_groupname
        else:
            window.close()
            result = None

def create_gui(text_data):
    for text in text_data:
        checkbox = QCheckBox(text)
        checkbox_values.append(checkbox)
        layout.addWidget(checkbox)

    global new_group_input
    new_group_input = QLineEdit()
    new_group_input.setPlaceholderText("Neuer Gruppenname")
    layout.addWidget(new_group_input)

    ok_button = QPushButton("OK")
    ok_button.clicked.connect(on_checkbox_click)
    layout.addWidget(ok_button)

    window.setLayout(layout)
    window.show()

checkbox_values = []

def SaveGruppeName(Neuer_Gruppename_eintrag, path_text):
    with open(path_text, "a", encoding="cp1252") as Animetexteintragneu:
        Animetexteintragneu.write("\n" + Neuer_Gruppename_eintrag)

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
                    SaveGruppeName(Gruppename, path_text)
                    return "-" + Gruppename
                else:
                    return "-" + Gruppename
            else:
                create_gui(text_data)
                app.exec_()
                return "-" + result