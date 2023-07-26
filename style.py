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
