import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QListWidget, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from app import app
import glob
import os
import fnmatch
									  											  											
def delete_images(folder_path):

    app = QApplication.instance()  # Versuchen Sie, eine vorhandene QApplication-Instanz abzurufen
    if app is None:
        app = QApplication([])  # Wenn keine vorhanden ist, erstellen Sie eine neue

    print("\nAktueller Ordner:", folder_path)
    image_extensions = ["jpg", "png", "gif", "bif", "nfo", "txt"]
    image_files = []
    for root, _, files in os.walk(folder_path):
        for extension in image_extensions:
            for filename in fnmatch.filter(files, f"*.{extension}"):
                image_files.append(os.path.join(root, filename))
    image_files

    if not image_files:
        print("Keine Bilder im angegebenen Ordner gefunden.")
        return

    class DeleteImagesGUI(QWidget):
        ok_clicked_deleteimages = QtCore.pyqtSignal()  # Signal für den Klick auf den "OK"-Button
        closed = QtCore.pyqtSignal()      # Signal für das Schließen des Fensters

        def closeEvent(self, event):
                # Wird aufgerufen, wenn das Fenster geschlossen wird
                self.closed.emit()
                print("Das GUI-Fenster wurde geschlossen.")
                event.accept()  # Bestätigen Sie das Ereignis, um das Fenster zu schließen    

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
                try:					 
                    if self.selected_extensions:
                        for file in image_files:
                            file_extension = os.path.splitext(file)[1][1:].lower()
                            if file_extension in self.selected_extensions:
                                os.remove(file)
                                self.list_widget.takeItem(self.list_widget.row(self.list_widget.findItems(file, QtCore.Qt.MatchExactly)[0]))
                    elif self.selected_files:
                        for file in self.selected_files:
                            os.remove(file)
                            self.list_widget.takeItem(self.list_widget.row(self.list_widget.findItems(file, QtCore.Qt.MatchExactly)[0]))

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
    return

if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Test\Demon.Slayer.Kimetsu"
    if not os.path.exists(path):
        print(f"Der angegebene Pfad '{path}' existiert nicht.")
    else:
        delete_images(path)
