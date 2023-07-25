import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal

app = QApplication.instance()
if app is None:
    app = QApplication([])

class GruppnameGUI(QWidget):
    ok_clicked = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, text_data, path_text):
        super().__init__()
        self.setWindowTitle("Gruppennamen auswählen")
        self.setGeometry(100, 100, 400, 300)
        self.text_data = text_data
        self.path_text = path_text  # Neue Instanzattribut, um den Pfad zur Textdatei zu speichern

        layout = QVBoxLayout()

        self.checkbox_values = []
        for text in self.text_data:
            checkbox = QCheckBox(text)
            self.checkbox_values.append(checkbox)
            layout.addWidget(checkbox)

        self.new_group_input = QLineEdit()
        self.new_group_input.setPlaceholderText("Neuer Gruppenname")
        layout.addWidget(self.new_group_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.on_ok_button_click)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.result = None   

    def on_ok_button_click(self):
        selected_text = [self.text_data[i] for i, value in enumerate(self.checkbox_values) if value.isChecked()]
        if selected_text:
            gruppename = "-".join(selected_text)
            self.result = gruppename
        else:
            new_groupname = self.new_group_input.text()
            if new_groupname:
                self.result = new_groupname
                # Neuer Gruppenname wird in die Textdatei geschrieben
                with open(self.path_text, "a", encoding="cp1252") as file:
                    file.write("\n" + new_groupname)
            else:
                self.result = None

        self.ok_clicked.emit()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()        

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
        if any(file.lower().endswith(ext) for ext in SourceList):
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
                gui = GruppnameGUI(text_data, path_text)
                gui.ok_clicked.connect(gui.close)
                gui.closed.connect(gui.close)
                gui.show()
                app.exec_()
                return "-" + gui.result

    return ""

if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test\Demon.Slayer.Kimetsu"
    path_text = r"C:\Users\admin\Desktop\Gruppen.txt"
    SourceList = ["mp4", "mkv"]
    if not path:
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
    else:
        gruppe = finde_groupname(path, SourceList, path_text)
        print(gruppe)
