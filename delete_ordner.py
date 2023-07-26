import os
import shutil
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, QMessageBox
from app import app
from style import apply_dark_theme

def has_subfolders(folder_path):
    subfolders = [f for f in os.scandir(folder_path) if f.is_dir()]
    return len(subfolders) > 0
    apply_dark_theme(app)

class DeleteFoldersGUI(QWidget):
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.setWindowTitle("Ordner löschen?")
        self.setGeometry(100, 100, 400, 400)
        apply_dark_theme(app)

        layout = QVBoxLayout()

        label = QLabel(f"Ordner: {self.folder_path}")
        layout.addWidget(label)

        self.folder_contents = [f for f in os.scandir(self.folder_path) if f.is_dir()]
        self.list_widget = QListWidget()
        self.list_widget.addItems([f.name for f in self.folder_contents])
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)  # Multi-Selection aktivieren
        layout.addWidget(self.list_widget)

        view_button = QPushButton("Ordner ansehen")
        view_button.clicked.connect(self.view_folder)
        view_button.setStyleSheet("background-color: #2a82da; color: white;")
        layout.addWidget(view_button)

        delete_button = QPushButton("Löschen")
        delete_button.clicked.connect(self.delete_folders)
        delete_button.setStyleSheet("background-color: #da2a2a; color: white;")
        layout.addWidget(delete_button)

        close_button = QPushButton("Schließen")
        close_button.clicked.connect(self.close_button_clicked)
        close_button.setStyleSheet("background-color: #595959; color: white;")
        layout.addWidget(close_button)

        self.setLayout(layout)

    def view_folder(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte wählen Sie mindestens einen Ordner zum Anzeigen aus.")
            return

        for item in selected_items:
            folder_name = item.text()
            folder_path = os.path.join(self.folder_path, folder_name)

            try:
                os.startfile(folder_path)  # Öffnet den Ordner im Datei-Explorer (für Windows)
            except Exception as e:
                QMessageBox.critical(self, "Fehler beim Öffnen", f"Fehler beim Öffnen von '{folder_name}': {str(e)}")

    def delete_folders(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte wählen Sie mindestens einen Ordner zum Löschen aus.")
            return

        confirm_delete = QMessageBox.question(self, "Löschen bestätigen", "Sind Sie sicher, dass Sie die ausgewählten Ordner löschen möchten?",
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm_delete == QMessageBox.Yes:
            for item in selected_items:
                folder_name = item.text()
                folder_path = os.path.join(self.folder_path, folder_name)

                try:
                    shutil.rmtree(folder_path)  # Löscht den Ordner mit seinem Inhalt
                except Exception as e:
                    QMessageBox.critical(self, "Fehler beim Löschen", f"Fehler beim Löschen von '{folder_name}': {str(e)}")

            self.list_widget.clear()
            self.folder_contents = [f for f in os.scandir(self.folder_path) if f.is_dir()]
            self.list_widget.addItems([f.name for f in self.folder_contents])

            if not self.folder_contents:
                self.close()

    def close_button_clicked(self):
        self.close()

def delete_ordner(folder_path):    
    if has_subfolders(folder_path):
        gui = DeleteFoldersGUI(folder_path)
        gui.show()
        app.exec_()
    else:
        print("Es gibt keine Subfolger zum Löschen.")

if __name__ == "__main__":
    folder_path = r"C:\Users\admin\Desktop\test\Double J"
    delete_ordner(folder_path)

