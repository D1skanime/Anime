import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QListWidget, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import glob
import os


def delete_images(folder_path):
    print("\nAktueller Ordner:", folder_path)
    image_extensions = ["jpg", "png", "gif", "bif", "nfo", "txt"]
    image_files = []
    for extension in image_extensions:
        image_files.extend(glob.glob(folder_path + "/*." + extension))

    if not image_files:
        return

    class DeleteImagesGUI(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Bilder löschen")
            self.setGeometry(100, 100, 600, 500)

            layout = QVBoxLayout()

            label = QLabel("Gefundene Dateien:")
            layout.addWidget(label)
            layout.setSpacing(10)

            checkbox_frame = QWidget()
            checkbox_layout = QVBoxLayout(checkbox_frame)
            checkboxes = []
            selected_extensions = []

            def toggle_extension(extension):
                if extension in selected_extensions:
                    selected_extensions.remove(extension)
                else:
                    selected_extensions.append(extension)

            for extension in image_extensions:
                if any(file.endswith("." + extension) for file in image_files):
                    checkbox = QCheckBox(extension)
                    checkbox.stateChanged.connect(lambda state, ext=extension: toggle_extension(ext))
                    checkbox_layout.addWidget(checkbox)
                    checkboxes.append(checkbox)

            layout.addWidget(checkbox_frame)

            list_widget = QListWidget()
            list_widget.setSelectionMode(QListWidget.MultiSelection)
            layout.addWidget(list_widget)
            for file in image_files:
                list_widget.addItem(file)

            delete_button = QPushButton("Ausgewählte löschen")
            delete_button.clicked.connect(self.delete_selected)
            layout.addWidget(delete_button)

            self.setLayout(layout)

            self.selected_files = []
            self.selected_extensions = selected_extensions
            self.list_widget = list_widget

        def delete_selected(self):
            selected_items = self.list_widget.selectedItems()
            self.selected_files = [item.text() for item in selected_items]

            if self.selected_files or self.selected_extensions:
                if self.selected_extensions:
                    for file in image_files:
                        file_extension = os.path.splitext(file)[1][1:].lower()
                        if file_extension in self.selected_extensions:
                            try:
                                os.remove(file)
                                self.list_widget.takeItem(self.list_widget.row(self.list_widget.findItems(file, QtCore.Qt.MatchExactly)[0]))
                            except OSError as e:
                                QMessageBox.critical(None, "Fehler beim Löschen", f"Fehler beim Löschen der Datei {file}: {e.strerror}")
                elif self.selected_files:
                    for file in self.selected_files:
                        try:
                            os.remove(file)
                            self.list_widget.takeItem(self.list_widget.row(self.list_widget.findItems(file, QtCore.Qt.MatchExactly)[0]))
                        except OSError as e:
                            QMessageBox.critical(None, "Fehler beim Löschen", f"Fehler beim Löschen der Datei {file}: {e.strerror}")

            self.close()

    app = QApplication(sys.argv)
    gui = DeleteImagesGUI()
    gui.show()
    app.exec_()

    return gui.selected_files, gui.selected_extensions