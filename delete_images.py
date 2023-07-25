import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QImageReader, QIcon, QImage
from PyQt5 import QtCore
import os
import fnmatch


def delete_images(folder_path):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    print("\nAktueller Ordner:", folder_path)
    image_extensions = ["nfo", "txt", "jpg", "png", "gif", "bif"]
    image_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            for extension in image_extensions:
                if filename.lower().endswith("." + extension):
                    image_files.append(file_path)

    if not image_files:
        print("Keine Bilder im angegebenen Ordner gefunden.")
        return

    def sort_by_extension(file):
        _, ext = os.path.splitext(file)
        return image_extensions.index(ext[1:].lower())

    image_files.sort(key=sort_by_extension)

    class ImagePreviewItem(QWidget):
        def __init__(self, file_path):
            super().__init__()
            self.file_path = file_path
            self.init_ui()

        def init_ui(self):
            layout = QHBoxLayout()

            label = QLabel(os.path.basename(self.file_path))
            layout.addWidget(label)

            thumbnail = self.generate_thumbnail()
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(thumbnail)
            layout.addWidget(thumbnail_label)

            self.setLayout(layout)

        def generate_thumbnail(self):
            image_reader = QImageReader(self.file_path)
            image_reader.setAutoTransform(True)
            image = image_reader.read()
            thumbnail = image.scaledToWidth(200, QtCore.Qt.SmoothTransformation)
            return QPixmap.fromImage(thumbnail)

    class DeleteImagesGUI(QWidget):
        ok_clicked_deleteimages = QtCore.pyqtSignal()
        closed = QtCore.pyqtSignal()

        def closeEvent(self, event):
            self.closed.emit()
            print("Das GUI-Fenster wurde geschlossen.")
            event.accept()

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
                item = QListWidgetItem(list_widget)
                widget = ImagePreviewItem(file)
                list_widget.setItemWidget(item, widget)
                item.setSizeHint(widget.sizeHint())
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)  # Disable item selection
                item.setSizeHint(QtCore.QSize(220, 220))  # Set fixed size for each item
                item.file_path = file  # Set the file_path attribute
            delete_button = QPushButton("Ausgewählte löschen")
            delete_button.clicked.connect(self.delete_selected)
            layout.addWidget(delete_button)
            self.setLayout(layout)
            self.selected_files = []
            self.selected_extensions = selected_extensions
            self.list_widget = list_widget

        def delete_selected(self):
            selected_items = self.list_widget.selectedItems()
            self.selected_files = [item.file_path for item in selected_items]

            if self.selected_files or self.selected_extensions:
                try:
                    if self.selected_extensions:
                        for file in image_files:
                            file_extension = os.path.splitext(file)[1][1:].lower()
                            if file_extension in self.selected_extensions:
                                os.remove(file)
                    elif self.selected_files:
                        for file in self.selected_files:
                            os.remove(file)

                except OSError as e:
                    error_message = f"Fehler beim Löschen der Datei {file}: {e.strerror}"
                    QMessageBox.critical(None, "Fehler beim Löschen", error_message)
                    print(error_message)
            self.close()

    gui = DeleteImagesGUI()
    gui.ok_clicked_deleteimages.connect(gui.close)
    gui.closed.connect(gui.close)
    gui.show()
    app.exec_()


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test\Demon.Slayer.Kimetsu"
    if not os.path.exists(path):
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
    else:
        delete_images(path)
