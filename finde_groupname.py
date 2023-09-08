import os
import re
import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLineEdit, QScrollArea, QLabel, QDesktopWidget
from PyQt5.QtCore import pyqtSignal
from app import app
from style import apply_dark_theme

app = QApplication.instance()
if app is None:
    app = QApplication([])

    # Bildschirmgröße ermitteln
screen = QDesktopWidget().screenGeometry()
screen_width = screen.width()
screen_height = screen.height()


    # GUI-Größe um 10 Prozent kleiner setzen
gui_width = int(screen_width * 0.5)
gui_height = int(screen_height * 0.9) 

apply_dark_theme(app)

import getpass
print(getpass.getuser())

class GruppnameGUI(QWidget):
    ok_clicked = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self, text_data, path_text, new_keys_to_add, animename):
        super().__init__()
        self.setWindowTitle("Gruppennamen auswählen")
        self.setGeometry(100, 100, gui_width, gui_height)
        self.text_data = sorted(text_data)
        self.path_text = path_text  # Neue Instanzattribut, um den Pfad zur Textdatei zu speichern
        self.animename = animename

        layout = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        self.new_keys_to_add = new_keys_to_add
        self.label_values = []

        if new_keys_to_add:
            keys_label = QLabel("New Keys to Add:")
            keys_label.setStyleSheet("color: white; font-weight: bold;")
            layout.addWidget(keys_label)

            for key in new_keys_to_add:
                key_label = QLabel(key)
									  
                key_label.setStyleSheet("color: white;")
																													
                self.label_values.append(key_label)
                layout.addWidget(key_label)



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
        ok_button.clicked.connect(lambda: self.on_ok_button_click(animename))
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.result = None

    def on_checkbox_clicked(self, checkbox, checked):
        if checked:
            for other_checkbox in self.checkbox_values:
                if other_checkbox != checkbox:
                    other_checkbox.setChecked(False)   

    def on_ok_button_click(self, animename):
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
            if self.new_keys_to_add:
                for key in self.new_keys_to_add:
                    animename[key].append("-" + gruppename)
        else:
            new_groupname = self.new_group_input.text()
            if new_groupname:
                self.result = new_groupname
                if self.new_keys_to_add:
                    for key in self.new_keys_to_add:
                        animename[key].append("-" + new_groupname)
                SaveGruppeName(new_groupname, self.path_text)
                SaveGruppeName(self.result, self.path_text)
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
def finde_groupname(path_text, animename):
    text_data = []
    with open(path_text, 'r', encoding="cp1252") as file:
        text_data = [_.rstrip('\n') for _ in file]
    new_keys_to_add = []
    for file in animename.keys():
        match = re.search(r"^\[(.*?)\]|(?<=-)[A-Za-z0-9_-]+(?=\.)", file)
        if match:
            Gruppename = match.group(0)
            pattern = r"\b" + re.escape(Gruppename) + r"\b"
            SonderzeichenListe = ["/", "?", "*", "<", ">", "'", "|", ":", "[", "]"]
            for SonderZeichen in SonderzeichenListe:
                Gruppename = Gruppename.replace(SonderZeichen, "!" if SonderZeichen == "?" else "")
            if not re.search(pattern, ' '.join(text_data)):
                SaveGruppeName(Gruppename, path_text)
                animename[file].append("-" + Gruppename)
            else:
                animename[file].append("-" + Gruppename)
        else:
            new_keys_to_add.append(file)

    if new_keys_to_add:
        gui = GruppnameGUI(text_data, path_text,new_keys_to_add,animename)
        gui.ok_clicked.connect(gui.close)
        gui.closed.connect(gui.close)
        gui.show()
        app.exec_()
        

    return animename

if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\test\11eyes"
    path_text = r"C:\Users\admin\Desktop\Gruppen.txt"
    SourceList = ["mp4", "mkv", "avi"]
    animename = {'11 Eyes.S01E01-B-SH.mkv': ['Test', '01'], '11 Eyes.S01E01-Strawhat.mkv': ['Test', '01'], '11 Eyes.S01E02-Strawhat.mkv': ['Test', '02'], '11 Eyes.S01E02.mkv': ['Test', '02'], '11 Eyes.S01E03-B-SH.mkv': ['Test', '03'], '11 Eyes.S01E03-Strawhat.mkv': ['Test', '03'], '11 Eyes.S01E04-B-SH.mkv': ['Test', '04'], '11 Eyes.S01E04-Strawhat.mkv': ['Test', '04'], '11 Eyes.S01E05-B-SH.mkv': ['Test', '05'], '11 Eyes.S01E05-Strawhat.mkv': ['Test', '05'], '11 Eyes.S01E06-B-SH.mkv': ['Test', '06'], '11 Eyes.S01E06-Strawhat.mkv': ['Test', '06'], '11 Eyes.S01E07-B-SH.mkv': ['Test', '07'], '11 Eyes.S01E07-Strawhat.mkv': ['Test', '07']}
    animename = finde_groupname(path, SourceList, path_text, animename)
    print(animename)

