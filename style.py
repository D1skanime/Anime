from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5 import QtCore

def apply_dark_theme(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(dark_palette)

    font = QFont("Arial", 10)
    app.setFont(font)

    app.setStyleSheet("""
        QPushButton {
            background-color: #353535;
            color: white;
            border: none;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #454545;
        }
        QPushButton:pressed {
            background-color: #252525;
        }
        QPushButton#primary {
    background-color: #2a82da; border: 1px solid #2a82da; color: #fff;
}
QPushButton#primary:hover { background-color: #3b8ee6; }

QPushButton#danger  {
    background-color: #c75050; border: 1px solid #c75050; color: #fff;
}
QPushButton#danger:hover { background-color: #d55e5e; } 
QLineEdit, QComboBox, QSpinBox, QDateEdit {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #8c8c8c;
    border-radius: 4px;
    padding: 4px 6px;
    selection-background-color: #2a82da;
    selection-color: #ffffff;
}

/* Dropdown-Liste der ComboBox ebenfalls lesbar */
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #000000;
    selection-background-color: #2a82da;
    selection-color: #ffffff;
}
    """)
