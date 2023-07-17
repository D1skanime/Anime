import os
import re
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox


class FolderNameGUI(QWidget):
    def __init__(self, inhalt):
        super().__init__()
        self.setWindowTitle("Ordnerbenennung")
        
        layout = QVBoxLayout()
        
        label = QLabel("Ordnername eingeben:")
        layout.addWidget(label)
        
        self.entry = QLineEdit()
        self.entry.setText(inhalt)
        layout.addWidget(self.entry)
        
        button = QPushButton("OK")
        button.clicked.connect(self.handle_button_click)
        layout.addWidget(button)
        
        self.setLayout(layout)
        self.new_folder_name = ""

    def handle_button_click(self):
        self.new_folder_name = self.entry.text()
        self.close()


def load_gui_and_get_folder_name(inhalt):
    app = QApplication(sys.argv)
    gui = FolderNameGUI(inhalt)
    gui.show()
    app.exec_()
    
    return gui.new_folder_name


SonderzeichenListe = ["/", "?", "*", "<", ">", "''", "|", ":"]

# Funktion zum Umbenennen des Ordners wie Anime oder neuer Name
def Ordnername(inhalt):
    newOrdnerAnimename = load_gui_and_get_folder_name(inhalt)
    newOrdnerAnimename = KillSpezialBuchtaben(newOrdnerAnimename)
    return newOrdnerAnimename


def KillSpezialBuchtaben(Animename):
    for SonderZeichen in SonderzeichenListe:
        if Animename.find(SonderZeichen) != -1:
            if SonderZeichen == "?":
                Animename = Animename.replace(SonderZeichen, "!")
            else:
                Animename = Animename.replace(SonderZeichen, "")
    return Animename
