import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QSpinBox
from PyQt5.QtCore import pyqtSignal
from app import app
from style import apply_dark_theme

class TagSourceGUI(QWidget):
    ok_clicked = pyqtSignal()
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI")
        apply_dark_theme(app)  # Anwendung des dunklen Themes (falls gewünscht)
        
        layout = QVBoxLayout()
        
        select_label = QLabel("Wert:")
        select_label.setStyleSheet("color: white; font-weight: bold;")  # Weiße Schrift auf dunklem Hintergrund
        layout.addWidget(select_label)
        
        self.select_box = QComboBox()
        self.select_box.addItems(["Serie", "Film", "Bonus", "OVA", "Web", "ONA", "Tv-Spezial", "AMV"])
        self.select_box.setStyleSheet("background-color: #f0f0f0; color: black; font-size: 12px;")  # Helles Grau für Hintergrund und schwarzer Text
        self.select_box.setCurrentIndex(0)
        layout.addWidget(self.select_box)
        
        self.counter_label = QLabel("Counter:")
        self.counter_label.setStyleSheet("color: white; font-weight: bold;")  # Weiße Schrift auf dunklem Hintergrund
        layout.addWidget(self.counter_label)
        
        self.counter = QSpinBox()
        self.counter.setStyleSheet("background-color: #f0f0f0; color: black; font-size: 12px;")  # Helles Grau für Hintergrund und schwarzer Text
        self.counter.setMinimum(0)
        self.counter.setMaximum(999)
        self.counter.setValue(1)
        layout.addWidget(self.counter)
        
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")  # Blaue Schaltfläche mit weißem Text
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
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        apply_dark_theme(app)  # Anwendung des dunklen Themes (falls gewünscht)

    gui = TagSourceGUI()
    gui.ok_clicked.connect(app.quit)  # Verwenden Sie app.quit anstelle von app.exit
    gui.closed.connect(app.quit)
    gui.show()
    app.exec_()
    return gui.formatted_value, gui.selected_value

if __name__ == "__main__":
    formatted_value, selected_value = tag_source()
    print("Formatted Value:", formatted_value)
    print("Selected Value:", selected_value)
