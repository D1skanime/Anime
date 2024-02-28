from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QVBoxLayout, QScrollArea, QGridLayout, QLineEdit, QDateEdit, QMessageBox, QSizePolicy, QComboBox,QHBoxLayout, QMainWindow
from PyQt5.QtCore import QSize, Qt
import sys

from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(QMainWindow):
    def __init__(self, videofiles, gruppenliste):
        super().__init__()
        self.videofiles = videofiles
        self.gruppenliste = gruppenliste
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1174, 660)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(7, 1, 269, 179))
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        save_button = QPushButton("Speichern")
        save_button.clicked.connect(self.save_changes)
        save_button.setGeometry(QtCore.QRect(10, 594, 1151, 30))
        save_button.setParent(self.centralwidget)  # Button-Widget zum Zentralwidget hinzufügen

    def save_changes(self):
        print("Speichern geklickt!")
        #Die self.close  wird nicht ausgeführt die gui bleibt bestehn nach dem speichern geht der code nicht zu print Videofiles
        print(self.close())
        # was auch immer hier mit self.videofiles passieren soll.

def create_gui(videofiles, gruppenliste):
    app = QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow(videofiles, gruppenliste)
    ui.show()
    app.exec_()
    return ui.videofiles

if __name__ == "__main__":
    gruppenliste = ['aaa', 'bbbb', 'cc']

    videofiles = {
        'MM__01.mkv': ['Testffffffffffffffffffffffff', 'A Town Where You Live.', 'AMV', '', '02', '01', 'GruppeKampfkuchen', '.mkv'],
        'MM__02.mkv': ['Test', 'A Town Where You Live.', 'Film', '2012', '02', '02', 'GruppeKampfkuchen', '.mkv'],
        'MM__03.mkv': ['Test', 'A Town Where You Live.', '', '', '02', '03', 'GruppeKampfkuchen', '.mkv'],
    }

    videofiles = create_gui(videofiles, gruppenliste)
    print(videofiles)