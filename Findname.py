import os
import re
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox

class FolgenlisteGUI(QWidget):
    def __init__(self, files, videofiles):
        super().__init__()
        self.setWindowTitle("Folgenliste")
        
        layout = QVBoxLayout()
        
        self.entry_boxes = []
        for file in sorted(videofiles, key=lambda x: int(videofiles[x][1])):
            folge_name = file
            folge_nummer = videofiles[file][1]

            label = QLabel(folge_name)
            layout.addWidget(label)

            entry_box = QLineEdit()
            entry_box.setText(folge_nummer)
            layout.addWidget(entry_box)

            self.entry_boxes.append(entry_box)

        save_button = QPushButton("OK")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.files = files
        self.videofiles = videofiles

    def save_changes(self):
        for i, file in enumerate(sorted(self.videofiles, key=lambda x: int(self.videofiles[x][1]))):
            new_folge_nummer = self.entry_boxes[i].text()
            try:
                nummer = int(new_folge_nummer)
                if 0 <= nummer <= 999:
                    if new_folge_nummer != self.videofiles[file][1]:
                        self.videofiles[file][1] = new_folge_nummer
                else:
                    QMessageBox.critical(self, "Ungültige Eingabe", "Die Folgennummer muss eine ganze Zahl zwischen 0 und 999 sein.")
                    return
            except ValueError:
                QMessageBox.critical(self, "Ungültige Eingabe", "Die Folgennummer muss eine ganze Zahl sein.")
                return
        self.close()


def findname(path, animename, sourcelist):
    files = os.listdir(path)
    videofiles = {}
    for file in files:
        video_sourcetype = source(file, sourcelist)
        if video_sourcetype:
            videofiles[file] = [animename]
            folge_nummer = find_folge_nummer(file)
            videofiles[file].append(folge_nummer)
            print(file, "-------", folge_nummer)

    if video_sourcetype:
        updated_files = create_gui(files, videofiles)
        return updated_files


def create_gui(files, videofiles):
    app = get_application_instance()
    gui = FolgenlisteGUI(files, videofiles)
    gui.show()
    app.exec_()
    
    return gui.videofiles


def source(filename, sourcelist):
    for source in sourcelist:
        if filename.lower().endswith(source):
            return source
    return None


def find_folge_nummer(filename):
    # Muster SxxExx
    match = re.search(r"S\d{2}E(\d{2})", filename)
    if match:
        folge_nummer = match.group(1)
        return folge_nummer
    # Muster SxxExxx
    match = re.search(r"S\d{2}E(\d{3})", filename)
    if match:
        folge_nummer = match.group(1)
        return folge_nummer
    # Ignoriert []{}()
    match = re.search(r"\b(\d+)\b(?!\.\w+$)(?![\[\(\{]).*?$", filename[::-1])
    if match:
        folge_nummer = match.group(1)[::-1]
        return folge_nummer
    # Muster 00x erkennen
    match = re.search(r"(\d{2,})\D*$", filename[::-1])
    if match:
        folge_nummer = match.group(1)[::-1]
        return folge_nummer
    return 0

def get_application_instance():
    app = QApplication.instance()  # Versuchen Sie, eine vorhandene QApplication-Instanz abzurufen
    if app is None:  # Wenn keine vorhanden ist, erstellen Sie eine neue
        app = QApplication(sys.argv)
    return app

if __name__ == "__main__":
    # Hier sollte der Code aufgerufen werden, indem der entsprechende Pfad und die SourceListe übergeben werden.
    # Beispiel: findname("Pfad_zum_Verzeichnis", "Animename", [".mp4", ".mkv"])
    pass
