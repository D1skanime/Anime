import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QSpinBox
from PyQt5.QtCore import pyqtSignal
from app import app

class TagSourceGUI(QWidget):
    ok_clicked = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI")
        self.setStyleSheet("background-color: lightgray;")
        
        layout = QVBoxLayout()
        
        select_label = QLabel("Wert:")
        select_label.setStyleSheet("color: blue; font-weight: bold;")
        layout.addWidget(select_label)
        
        self.select_box = QComboBox()
        self.select_box.addItems(["Serie", "Film", "Bonus", "OVA", "Web", "ONA", "Tv-Spezial","AMV"])
        self.select_box.setStyleSheet("background-color: white;")
        self.select_box.setCurrentIndex(0)
        layout.addWidget(self.select_box)
        
        self.counter_label = QLabel("Counter:")
        self.counter_label.setStyleSheet("color: blue; font-weight: bold;")
        layout.addWidget(self.counter_label)
        
        self.counter = QSpinBox()
        self.counter.setStyleSheet("background-color: white;")
        self.counter.setMinimum(0)
        self.counter.setMaximum(999)
        self.counter.setValue(1)
        layout.addWidget(self.counter)
        
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")
        ok_button.clicked.connect(self.ok_button_click)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)
        self.formatted_value = ""
        self.selected_value = ""

    def ok_button_click(self):
        self.selected_value = self.select_box.currentText()

        if self.selected_value in ["AMV", "Film"]:
            self.formatted_value = ""
            self.counter_label.hide()
            self.counter.hide()
        else:
            if self.selected_value == "Serie":
                self.selected_value = ""
            counter_value = self.counter.value()
            if counter_value < 10:
                self.formatted_value = 'S0' + str(counter_value)
            else:
                self.formatted_value = 'S' + str(counter_value)
                
        self.ok_clicked.emit()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
        



def tag_source():
    app = QApplication.instance()  # Versuchen Sie, eine vorhandene QApplication-Instanz abzurufen
    if app is None:     
       app = QApplication([])

      # Erstellen Sie eine neue QApplication-Instanz
    gui = TagSourceGUI()
    gui.ok_clicked.connect(app.exit)  # Verwenden Sie app.quit anstelle von app.exit
    gui.closed.connect(app.exit)
    gui.show()
    app.exec_()
    return gui.formatted_value, gui.selected_value

    

