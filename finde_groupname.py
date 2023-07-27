import os
import re
import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLineEdit, QScrollArea
from PyQt5.QtCore import pyqtSignal
from app import app
from style import apply_dark_theme

app = QApplication.instance()
if app is None:
    app = QApplication([])
apply_dark_theme(app)

class GruppnameGUI(QWidget):
    ok_clicked = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, text_data, path_text):
        super().__init__()
        self.setWindowTitle("Gruppennamen auswählen")
        self.setGeometry(100, 100, 400, 300)
        self.text_data = sorted(text_data)
        self.path_text = path_text  # Neue Instanzattribut, um den Pfad zur Textdatei zu speichern

        layout = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        self.checkbox_values = []
        for text in self.text_data:
            checkbox = QCheckBox(text)
            checkbox.setStyleSheet("color: white; font-weight: bold;")  # Weiße Schrift auf dunklem Hintergrund
            checkbox.clicked.connect(lambda checked, checkbox=checkbox: self.on_checkbox_clicked(checkbox, checked))
            self.checkbox_values.append(checkbox)
            scroll_layout.addWidget(checkbox)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        self.new_group_input = QLineEdit()
        self.new_group_input.setPlaceholderText("Neuer Gruppenname")
        self.new_group_input.setStyleSheet("background-color: #f0f0f0; color: black; font-size: 12px;")  # Helles Grau für Hintergrund und schwarzer Text
        layout.addWidget(self.new_group_input)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")  # Blaue Schaltfläche mit weißem Text
        ok_button.clicked.connect(self.on_ok_button_click)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.result = None

    def on_checkbox_clicked(self, checkbox, checked):
        if checked:
            for other_checkbox in self.checkbox_values:
                if other_checkbox != checkbox:
                    other_checkbox.setChecked(False)   

    def on_ok_button_click(self):
        selected_text = [self.text_data[i] for i, value in enumerate(self.checkbox_values) if value.isChecked()]
        new_groupname = self.new_group_input.text().strip()

        if not selected_text and not new_groupname:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Fehlende Auswahl")
            msg_box.setText("Bitte wählen Sie eine Checkbox aus oder geben Sie einen neuen Gruppennamen ein.")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet("background-color: #333333; color: white; font-size: 14px;")
            ok_button = msg_box.addButton("OK", QMessageBox.AcceptRole)
            ok_button.setStyleSheet("background-color: #4285f4; color: white; font-size: 14px; padding: 5px 10px;")
            msg_box.exec_()
            return
        if selected_text:
            gruppename = "-".join(selected_text)
            self.result = gruppename
        else:
            new_groupname = self.new_group_input.text()
            if new_groupname:
                self.result = new_groupname
                SaveGruppeName(self.result, path_text)
                # Neuer Gruppenname wird in die Textdatei geschrieben
            else:
                self.result = None

        self.ok_clicked.emit()

    def closeEvent(self, event):
        selected_text = [self.text_data[i] for i, value in enumerate(self.checkbox_values) if value.isChecked()]
        new_groupname = self.new_group_input.text().strip()
        #Todo Wenn Selected oder Gruppename eingetragen und auf kreuzbutton geklickt expeption einbauen
        if not selected_text and not new_groupname:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Fehlende Auswahl")
            msg_box.setText("Bitte wählen Sie eine Checkbox aus oder geben Sie einen neuen Gruppennamen ein.")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStyleSheet("background-color: #333333; color: white; font-size: 14px;")
            ok_button = msg_box.addButton("OK", QMessageBox.AcceptRole)
            ok_button.setStyleSheet("background-color: #4285f4; color: white; font-size: 14px; padding: 5px 10px;")
            msg_box.exec_()
            event.ignore()
        else:
            event.accept()

        self.closed.emit()

def check_gruppenname_existence(new_groupname, path_text):
    with open(path_text, "r", encoding="cp1252") as file:
        for line in file:
            if re.fullmatch(r"\b" + re.escape(new_groupname) + r"\b", line.strip()):
                return True
    return False

def SaveGruppeName(Neuer_Gruppename_eintrag, path_text):
    Neuer_Gruppename_eintrag = Neuer_Gruppename_eintrag.strip()
    if not check_gruppenname_existence(Neuer_Gruppename_eintrag, path_text):
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
                SonderzeichenListe = ["/", "?", "*", "<", ">", "'", "|", ":","[","]"]
                for SonderZeichen in SonderzeichenListe:
                    Gruppename = Gruppename.replace(SonderZeichen, "!" if SonderZeichen == "?" else "")
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
    path = r"C:\Users\admin\Desktop\Test\nogruppe"
    path_text = r"C:\Users\admin\Desktop\Gruppen.txt"
    SourceList = ["mp4", "mkv", "avi"]
    gruppe = finde_groupname(path, SourceList, path_text)
    print(gruppe)

