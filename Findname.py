import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QScrollArea, QGridLayout, QLineEdit, QMessageBox
from PyQt5 import QtGui

class FolgenlisteGUI(QWidget):
    def __init__(self, files, videofiles):
        super().__init__()
        self.setWindowTitle("Folgenliste")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        self.entry_boxes = []
        count = 0
        group_layout = None
        grid_layout = QGridLayout()
        for file in sorted(videofiles, key=lambda x: int(videofiles[x][1])):
            folge_name = file
            folge_nummer = videofiles[file][1]

            label = QLabel(folge_name)
            entry_box = QLineEdit()
            entry_box.setValidator(QtGui.QIntValidator(0, 999))
            entry_box.setText(folge_nummer)
            entry_box.setFixedWidth(entry_box.fontMetrics().boundingRect('8' * 3).width() + 10)
            entry_box.textChanged.connect(lambda text=entry_box: self.adjust_textfield_size(entry_box))  # Fix here

            row = count % 10
            col = count // 10

            grid_layout.addWidget(label, row * 2, col)
            grid_layout.addWidget(entry_box, row * 2 + 1, col)

            self.entry_boxes.append(entry_box)

            count += 1

        scroll_layout.addLayout(grid_layout)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

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

    def adjust_textfield_size(self, textfield):
        text = textfield.text()
        width = textfield.fontMetrics().boundingRect(text).width() + 10
        textfield.setFixedWidth(width)


def findname(path, animename, sourcelist):
    files = os.listdir(path)
    videofiles = {}
    for file in files:
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            continue
        video_sourcetype = source(file, sourcelist)
        if video_sourcetype is None:
            continue
        videofiles[file] = [animename]
        folge_nummer = find_folge_nummer(file)
        videofiles[file].append(folge_nummer)

    if video_sourcetype:
        updated_files = create_gui(files, videofiles)
        return updated_files


def create_gui(files, videofiles):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
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
    match = re.search(r"S\d{2}E(\d{2})", filename)
    if match:
        folge_nummer = match.group(1)
        return folge_nummer

    match = re.search(r"S\d{2}E(\d{3})", filename)
    if match:
        folge_nummer = match.group(1)
        return folge_nummer

    match = re.search(r"\b(\d+)\b(?!\.\w+$)(?![\[\(\{]).*?$", filename[::-1])
    if match:
        folge_nummer = match.group(1)[::-1]
        return folge_nummer

    match = re.search(r"(\d{2,})\D*$", filename[::-1])
    if match:
        folge_nummer = match.group(1)[::-1]
        return folge_nummer


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test\Dokidoki! Precure"
    animename = "Test"
    sourcelist = ["mp4", "mkv"]
    if not path:
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
    else:
        animename = findname(path, animename, sourcelist)
        print(animename)
