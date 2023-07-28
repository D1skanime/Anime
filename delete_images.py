import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QFont, QPixmap, QImageReader, QIcon, QImage, QPalette, QColor
from PyQt5 import QtCore
import os
import fnmatch
from style import apply_dark_theme


def delete_images(folder_path):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    apply_dark_theme(app)

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
            layout = QVBoxLayout()

            label = QLabel(os.path.basename(self.file_path))
            label.setAlignment(QtCore.Qt.AlignCenter)
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
            self.setGeometry(100, 100, 800, 600)

            main_layout = QVBoxLayout(self)

            layout = QHBoxLayout()

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
                    checkbox.setStyleSheet("color: white")
                    checkbox.stateChanged.connect(lambda state, ext=extension: toggle_extension(ext))
                    checkbox_layout.addWidget(checkbox)
                    checkboxes.append(checkbox)

            layout.addWidget(checkbox_frame)

            main_layout.addLayout(layout)

            label = QLabel("Gefundene Dateien:")
            label.setAlignment(QtCore.Qt.AlignCenter)
            main_layout.addWidget(label)

            scroll_area = QScrollArea()
            scroll_widget = QWidget()
            scroll_area.setWidget(scroll_widget)
            scroll_area.setWidgetResizable(True)
            scroll_layout = QVBoxLayout(scroll_widget)

            list_widget = QListWidget()
            list_widget.setSelectionMode(QListWidget.MultiSelection)
            scroll_layout.addWidget(list_widget)

            for file in image_files:
                item = QListWidgetItem(list_widget)
                widget = ImagePreviewItem(file)
                list_widget.setItemWidget(item, widget)
                item.setSizeHint(widget.sizeHint())
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)  # Disable item selection
                item.setSizeHint(QtCore.QSize(220, 220))  # Set fixed size for each item
                item.file_path = file  # Set the file_path attribute

            scroll_area.setMinimumHeight(220)
            layout.addWidget(scroll_area)

            delete_button = QPushButton("Ausgewählte löschen")
            delete_button.setStyleSheet("background-color: #3572A5; color: white; padding: 10px")
            delete_button.clicked.connect(self.delete_selected)
            main_layout.addWidget(delete_button)

            cancel_button = QPushButton("Abbrechen")
            cancel_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")  # Rote Schaltfläche mit weißem Text
            cancel_button.clicked.connect(self.on_cancel_clicked)
            layout.addWidget(cancel_button)

            self.selected_files = []
            self.selected_extensions = selected_extensions
            self.list_widget = list_widget

        def on_cancel_clicked(self):
            self.close()
           

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

            self.list_widget.clearSelection()

    gui = DeleteImagesGUI()
    gui.ok_clicked_deleteimages.connect(gui.close)
    gui.closed.connect(gui.close)
    gui.show()
    app.exec_()


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test\Demon.Slayer.Kimetsu"
    delete_images(path)
        
