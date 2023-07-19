import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox


class FolderNameGUI(QWidget):
    def __init__(self, inhalt, app):
        super().__init__()
        self.setWindowTitle("Ordnerbenennung")
        layout = QVBoxLayout()
        label = QLabel("Ordnername eingeben:")
        layout.addWidget(label)
        self.entry = QLineEdit(inhalt)
        layout.addWidget(self.entry)
        button = QPushButton("OK")
        button.clicked.connect(lambda: self.handle_button_click(app))  # app als Argument übergeben
        layout.addWidget(button)
        self.setLayout(layout)
        self.new_folder_name = inhalt

    def handle_button_click(self, app):  # app als Argument hinzufügen
        new_text = self.entry.text().strip()
        if new_text:
            self.new_folder_name = new_text
            self.close()
        else:
            QMessageBox.warning(self, "Eingabefehler", "Bitte geben Sie einen gültigen Ordnername ein.")

def load_gui_and_get_folder_name(inhalt):
    app = QApplication(sys.argv)
    gui = FolderNameGUI(inhalt, app)  # app als Argument übergeben
    gui.show()
    app.exec_()
    return gui.new_folder_name


SonderzeichenListe = ["/", "?", "*", "<", ">", "'", "|", ":"]

def Ordnername(inhalt):
    newOrdnerAnimename = load_gui_and_get_folder_name(inhalt)
    if not newOrdnerAnimename:
        raise ValueError("Ungültiger Ordnername: Der eingegebene Name ist leer.")
    
    for SonderZeichen in SonderzeichenListe:
        newOrdnerAnimename = newOrdnerAnimename.replace(SonderZeichen, "!" if SonderZeichen == "?" else "")
    return newOrdnerAnimename


