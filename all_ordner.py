import os
import shutil
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt
from app import app
from style import apply_dark_theme


class SelectFoldersGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ordner auswählen")
        self.setGeometry(100, 100, 200, 200)

        # Entferne die Schließen-, Verkleinern- und Vergrößern-Buttons
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowMinimizeButtonHint & ~Qt.WindowMaximizeButtonHint)

        apply_dark_theme(app)

        layout = QVBoxLayout()

        button_layout = QHBoxLayout()  # Erstelle ein Layout für die Buttons
        spacer_item = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum) 

        select_button_all = QPushButton("Alle Ordner auswählen")
        select_button_all.clicked.connect(self.all_folder)
        select_button_all.setStyleSheet("background-color: #2a82da; color: white;")
        select_button_all.setFixedSize(150, 150)
        button_layout.addWidget(select_button_all)

        button_layout.addSpacing(10)

        select_button = QPushButton("Ein Ordner auswählen")
        select_button.clicked.connect(self.one_folders)
        select_button.setStyleSheet("background-color: #da2a2a; color: white;")
        select_button.setFixedSize(140, 140)
        button_layout.addWidget(select_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def all_folder(self):
        self.result = "all"
        self.close()

    def one_folders(self):
        self.result = "one"
        self.close()

def all_ordner():    
        gui = SelectFoldersGUI()
        gui.show()
        desktop = QApplication.desktop()
        x = (desktop.width() - gui.width()) // 2
        y = (desktop.height() - gui.height()) // 2
        gui.move(x, y)
        app.exec_()
        return gui.result

if __name__ == "__main__":
    result= all_ordner()

