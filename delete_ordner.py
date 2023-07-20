import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, QMessageBox


def delete_all_ordner(Ordnerkill):
    Verzeichnisse_kill = [f.path for f in os.scandir(Ordnerkill) if f.is_dir()]
    for Verzechnis_kill in Verzeichnisse_kill:
        try:
            shutil.rmtree(Verzechnis_kill)
        except OSError as e:
            print(f"Error:{e.strerror}")
    return


class DeleteFoldersGUI(QWidget):
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.setWindowTitle("Ordner löschen?")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        label = QLabel(f"Ordner: {self.folder_path}")
        layout.addWidget(label)

        subfolders = [f.path for f in os.scandir(self.folder_path) if f.is_dir()]
        folder_contents = []
        for folder in subfolders:
            folder_contents.extend(os.listdir(folder))
        list_widget = QListWidget()
        list_widget.addItems(folder_contents)
        layout.addWidget(list_widget)

        delete_yes_button = QPushButton("Alle Ordner löschen (Ja)")
        delete_yes_button.clicked.connect(self.delete_yes)
        layout.addWidget(delete_yes_button)

        delete_no_button = QPushButton("Ordner nicht löschen (Nein)")
        delete_no_button.clicked.connect(self.delete_no)
        layout.addWidget(delete_no_button)

        self.setLayout(layout)

    def delete_yes(self):
        try:
            delete_all_ordner(self.folder_path)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Fehler beim Löschen", str(e))
            self.close()

    def delete_no(self):
        self.close()


if __name__ == "__main__":
    folder_path = "Pfad zum Ordner, dessen Inhalte gelöscht werden sollen"
else:
    def delete_ordner(item_path):
        app = QApplication([])
        gui = DeleteFoldersGUI(item_path)
        gui.show()
        app.exec_()
