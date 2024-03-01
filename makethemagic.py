import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QInputDialog, QDialog, QSizePolicy  # Importiere QSizePolicy
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QSize  
from PyQt5.QtGui import QPalette, QFont  
from app import app
from style import apply_dark_theme

apply_dark_theme(app)

class RenameDialog(QDialog):
    name_entered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neuer Dateiname")
        #self.setFixedSize(400, 150)  # Anfangsgröße festlegen
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)  # Setze die Größenrichtlinie des Dialogs auf Minimum

        layout = QVBoxLayout()

        self.label = QLabel("Datei existiert bereits")
        self.label.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(self.label)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Neuer Dateiname")
        layout.addWidget(self.line_edit)

        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet("font-size: 14px; padding: 6px; background-color: #4CAF50; color: white;")
        self.ok_button.clicked.connect(self.on_ok_button_clicked)
        layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setStyleSheet("font-size: 14px; padding: 6px; background-color: #f44336; color: white;")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        self.line_edit.setFocus()

        # Dunkles Hintergrund-Stylesheet für den Dialog und das Eingabefeld
        self.setStyleSheet("""
            QDialog {
                background-color: #333;
            }
            
            QLineEdit {
                background-color: #444;
                color: white;
                border: 1px solid #888;
                font-size: 14px;
                padding: 4px;
            }
        """)

    def on_ok_button_clicked(self):
        new_name = self.line_edit.text()
        self.name_entered.emit(new_name)
        self.accept()

    def get_new_name(self, Test_folgen):
        self.line_edit.setText(Test_folgen) 
        self.adjustSize()  
        result = self.exec_()  
        if result == QDialog.Accepted:
            return self.line_edit.text()
        else:
            return None

    def sizeHint(self):
        # Dynamische Größenanpassung basierend auf der Länge des Test_folgennamens
        font_metrics = self.line_edit.fontMetrics()
        text_width = font_metrics.boundingRect(self.line_edit.text()).width()
        return QSize(max(text_width + 150, 400), 150)


def makethemagic(path, videofiles):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    rename_dialog = RenameDialog()
    for file in sorted(videofiles.keys()):
        new_name = videofiles[file][8]
        folge_pfad = os.path.join(path, file)
        neue_folge_pfad = os.path.join(path, new_name)
        if folge_pfad == neue_folge_pfad:
            new_name = rename_dialog.get_new_name(new_name)
            if new_name is not None:
                neue_folge_pfad = os.path.join(path, new_name)
                os.replace(folge_pfad, neue_folge_pfad)
        else:
            try:
                os.rename(folge_pfad, neue_folge_pfad)
            except OSError as e:
                    QMessageBox.critical(None, "Fehler beim Umbenennen", f"Fehler beim Umbenennen von {new_name}: {e.strerror}")



if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\MM!"
    videofiles = {
        'A Town Where You Live.Bonus.S01E01-GruppeKampfkuchen.mkv': ['Testffffffffffffffffffffffff', 'A Town Where You Live', 'AMV', '', '02', '01-23', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E01-GruppeKampfkuchen.mkv'],
        'MM__02.mkv': ['Test', 'A Town Where You Live', 'Film', '2012', '02', '02', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E02-GruppeKampfkuchen.mkv'],
        'MM__03.mkv': ['Test', 'A Town Where You Live', '', '', '00', '03', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E03-GruppeKampfkuchen.mkv']
    }
    makethemagic(path, videofiles)
    print(videofiles)
