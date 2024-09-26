import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QVBoxLayout, QScrollArea, QGridLayout, QLineEdit, QDateEdit, QSizePolicy, QComboBox,QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
import subprocess
from app import app
from style import apply_dark_theme


class FolgenlisteGUI(QWidget):
    def __init__(self, videofiles, gruppenliste, typ_liste, path_ordner):
        super().__init__()
        self.setWindowTitle("Folgenliste")
        self.resize(1500, 600)
        apply_dark_theme(app)

        layout = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        self.entry_boxes = []


        # 1. Ordnername
        label_add_ordner_name = QLabel()
        label_add_ordner_name.setText("Ändere Ordnername")
        lineEdit_add_ordner_name = QLineEdit()
        lineEdit_add_ordner_name.setMinimumWidth(200)
        lineEdit_add_ordner_name.setText(videofiles[next(iter(videofiles))][0])
        lineEdit_add_ordner_name.setCursorPosition(0)

        pushButton_add_ordner_name = QPushButton("Übernehmen")
        pushButton_add_ordner_name.setObjectName("pushButton_add_ordner_name")
        pushButton_add_ordner_name, 0, 2, 1, 1
        pushButton_add_ordner_name.clicked.connect(lambda: self.insert_filename(lineEdit_add_ordner_name.text(),0))
        
        # Horizontales Layout für Ordnername erstellen
        add_layout_ordnername = QHBoxLayout()
        add_layout_ordnername.addWidget(label_add_ordner_name)
        add_layout_ordnername.addWidget(lineEdit_add_ordner_name)
        add_layout_ordnername.addWidget(pushButton_add_ordner_name)

        # Horizontales Layout dem Hauptlayout hinzufügen
        layout.addLayout(add_layout_ordnername)
        

        # 2. Dateiname
        label_add_videofile_name = QLabel()
        label_add_videofile_name.setObjectName("label_add_videofile_name")
        label_add_videofile_name.setText("Ändere Dateiname")

        lineEdit_add_videofile_name = QLineEdit()
        lineEdit_add_videofile_name.setObjectName("lineEdit_add_videofile_name")
        lineEdit_add_videofile_name.setText(videofiles[next(iter(videofiles))][1])
        lineEdit_add_videofile_name.setStyleSheet("color: black;")
        lineEdit_add_videofile_name.setCursorPosition(0)

        pushButton_add_videofile_name = QPushButton("Übernehmen")
        pushButton_add_videofile_name.setObjectName("pushButton_add_videofile_name")
        pushButton_add_videofile_name.clicked.connect(lambda: self.insert_filename(lineEdit_add_videofile_name.text(),1))

        # Horizontales Layout für Dateiname erstellen
        add_layout_dateiname = QHBoxLayout()
        add_layout_dateiname.addWidget(label_add_videofile_name)
        add_layout_dateiname.addWidget(lineEdit_add_videofile_name)
        add_layout_dateiname.addWidget(pushButton_add_videofile_name)

        # Horizontales Layout dem Hauptlayout hinzufügen
        layout.addLayout(add_layout_dateiname)

        #3. Type
        label_add_type = QLabel()
        label_add_type.setObjectName("label_add_type")
        label_add_type.setText("Ändere Type")

        comboBox_add_type = QComboBox()
        comboBox_add_type.setObjectName("comboBox_add_type")
        comboBox_add_type.addItem(videofiles[next(iter(videofiles))][2])
        comboBox_add_type.setEditText(videofiles[next(iter(videofiles))][2])
        comboBox_add_type.setStyleSheet("QComboBox { color: black; } QComboBox QAbstractItemView { background-color: #D3D3D3; color: black; }")
        comboBox_add_type.setEditable(True)
        comboBox_add_type.addItems(typ_liste)

        pushButton_add_type = QPushButton("Übernehmen")
        pushButton_add_type.setObjectName("pushButton_add_type")
        pushButton_add_type.clicked.connect(lambda: self.insert_filename(comboBox_add_type.currentText(),2))

        # Horizontales Layout für Dateiname erstellen
        add_layout_type = QHBoxLayout()
        add_layout_type.addWidget(label_add_type)
        add_layout_type.addWidget(comboBox_add_type)
        add_layout_type.addWidget(pushButton_add_type)
        layout.addLayout(add_layout_type)

        #4. Jahr
        label_add_jahr = QLabel()
        label_add_jahr.setObjectName("label_add_jahr")
        label_add_jahr.setText("Ändere Jahr")

        dateEdit_add_jahr = QDateEdit()
        dateEdit_add_jahr.setObjectName("dateEdit_add_jahr")
        dateEdit_add_jahr.setDate(QtCore.QDate.fromString(videofiles[next(iter(videofiles))][3], "yyyy"))
        dateEdit_add_jahr.setCalendarPopup(False)
        dateEdit_add_jahr.setDisplayFormat("yyyy")
        dateEdit_add_jahr.setStyleSheet("color: black;")


        pushButton_add_jahr = QPushButton("Übernehmen")
        pushButton_add_jahr.setObjectName("pushButton_add_jahr")
        pushButton_add_jahr.clicked.connect(lambda: self.insert_filename(dateEdit_add_jahr.date().toString("yyyy"),3))

        # Horizontales Layout für Dateiname erstellen
        add_layout_jahr = QHBoxLayout()
        add_layout_jahr.addWidget(label_add_jahr)
        add_layout_jahr.addWidget(dateEdit_add_jahr)
        add_layout_jahr.addWidget(pushButton_add_jahr)
        layout.addLayout(add_layout_jahr)

        #5. Staffel
        label_add_staffel = QLabel("Übernehmen")
        label_add_staffel.setObjectName("label_add_staffel")
        label_add_staffel.setText("Ändere Staffelnummer")

        spinBox_add_staffel = QSpinBox()
        spinBox_add_staffel.setObjectName("spinBox_add_staffel")
        spinBox_add_staffel.setMaximum(999)
        spinBox_add_staffel.setValue(int(videofiles[next(iter(videofiles))][4]))
        spinBox_add_staffel.setStyleSheet("color: black;")
            

        pushButton_add_staffel = QPushButton("Übernehmen")
        pushButton_add_staffel.setObjectName("pushButton_add_staffel")
        pushButton_add_staffel.clicked.connect(lambda: self.insert_filename(spinBox_add_staffel.value(),4))

        # Horizontales Layout für Dateiname erstellen
        add_layout_staffel = QHBoxLayout()
        add_layout_staffel.addWidget(label_add_staffel)
        add_layout_staffel.addWidget(spinBox_add_staffel)
        add_layout_staffel.addWidget(pushButton_add_staffel)
        layout.addLayout(add_layout_staffel)

        #6. Eingabefeld und Button für Episode-Auto-Fill
        label_episode_start = QLabel()
        label_episode_start.setText("Startwert für Episoden")

        lineEdit_episode_start = QLineEdit()
        lineEdit_episode_start.setMinimumWidth(100)
        lineEdit_episode_start.setStyleSheet("color: black;")


        pushButton_fill_episodes = QPushButton("Episoden automatisch füllen")
        pushButton_fill_episodes.clicked.connect(lambda: self.fill_episodes(int(lineEdit_episode_start.text())))

        # Horizontales Layout für Episoden-Auto-Fill erstellen
        add_layout_episode_fill = QHBoxLayout()
        add_layout_episode_fill.addWidget(label_episode_start)
        add_layout_episode_fill.addWidget(lineEdit_episode_start)
        add_layout_episode_fill.addWidget(pushButton_fill_episodes)
        layout.addLayout(add_layout_episode_fill)


        #7. Gruppe
        label_add_gruppe = QLabel()
        label_add_gruppe.setObjectName("label_add_gruppe")
        label_add_gruppe.setText("Ändere Gruppe")

        comboBox_add_gruppe = QComboBox()
        comboBox_add_gruppe.setObjectName("comboBox_add_gruppe")
        comboBox_add_gruppe.addItem(videofiles[next(iter(videofiles))][6])
        comboBox_add_gruppe.setEditText(videofiles[next(iter(videofiles))][6])
        comboBox_add_gruppe.setStyleSheet("QComboBox { color: black; } QComboBox QAbstractItemView { background-color: #D3D3D3; color: black; }")
        comboBox_add_gruppe.setEditable(True)
        comboBox_add_gruppe.addItems(gruppenliste)

        pushButton_add_gruppe = QPushButton('Übernehmen')
        pushButton_add_gruppe.setObjectName("pushButton_add_gruppe")
        pushButton_add_gruppe.clicked.connect(lambda: self.insert_filename(comboBox_add_gruppe.currentText(),6))

        # Horizontales Layout für Dateiname erstellen
        add_layout_gruppe = QHBoxLayout()
        add_layout_gruppe.addWidget(label_add_gruppe)
        add_layout_gruppe.addWidget(comboBox_add_gruppe)
        add_layout_gruppe.addWidget(pushButton_add_gruppe)
        layout.addLayout(add_layout_gruppe)

        #Path
        label_add_path = QLabel()
        label_add_path.setObjectName("label_add_path")
        label_add_path.setText("Schaue in den VidedateiOrdner")

        pushButton_add_path = QPushButton('Anzeigen')
        pushButton_add_path.setObjectName("pushButton_add_path")
        pushButton_add_path.clicked.connect(lambda: self.open_anime_folder(path_ordner))

        add_layout_path = QHBoxLayout()
        add_layout_path.addWidget(label_add_path)
        add_layout_path.addWidget(pushButton_add_path)
        layout.addLayout(add_layout_path)

        # Setzen des Hauptlayouts für das Widget
        self.setLayout(layout)

        # Labels hinzufügen
        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel("Ordner Name"))
        label_layout.addWidget(QLabel("Dateiname"))
        label_layout.addWidget(QLabel("Typ"))
        label_layout.addWidget(QLabel("Jahr"))
        label_layout.addWidget(QLabel("Staffel"))
        label_layout.addWidget(QLabel("Episode"))
        label_layout.addWidget(QLabel("Gruppe"))
        label_layout.addWidget(QLabel("Dateiendung"))
        layout.addLayout(label_layout)

        count = 0
        grid_layout = QGridLayout()
        for file in sorted(videofiles.keys()):
            ordner_name, dateiname, typ, jahr, staffel, episode, gruppe, dateiendung = videofiles[file]

            ordner_name_edit = QLineEdit(ordner_name)

            dateiname_edit = QLineEdit(dateiname)
            dateiname_edit.setMinimumWidth(200) 
            dateiname_edit.sizeHint = lambda: QSize(200, dateiname_edit.fontMetrics().height() + 6)
            dateiname_edit.adjustSize()

            comboBox_type = QComboBox()
            comboBox_type.addItem(typ)
            comboBox_type.setEditable(True)
            comboBox_type.addItems(typ_liste)
            comboBox_type.setEditText(typ)

            dateEdit_jahr = QDateEdit()
            dateEdit_jahr.setDate(QtCore.QDate.fromString(jahr, "yyyy"))
            dateEdit_jahr.setCalendarPopup(False)
            dateEdit_jahr.setDisplayFormat("yyyy")
            dateEdit_jahr.setStyleSheet("color: black;")

            spinBox_staffel = QSpinBox()
            spinBox_staffel.setMaximum(999)
            spinBox_staffel.setValue(int(staffel))
            spinBox_staffel.setStyleSheet("color: black;")
            
            Episode_edit = QLineEdit(episode)

            Gruppe_edit = QComboBox()
            Gruppe_edit.addItem(gruppe)
            Gruppe_edit.setEditable(True)
            Gruppe_edit.addItems(gruppenliste)
            Gruppe_edit.setEditText(gruppe)

            dateiendung_edit = QLineEdit(dateiendung)

            # Setze die Textfarbe auf Schwarz
            ordner_name_edit.setStyleSheet("color: black;")
            dateiname_edit.setStyleSheet("color: black;")
            comboBox_type.setStyleSheet("QComboBox { color: black; }")
            comboBox_type.view().setStyleSheet("QComboBox QAbstractItemView { background-color: #D3D3D3; color: black;}")
            dateEdit_jahr.setStyleSheet("color: black;")
            spinBox_staffel.setStyleSheet("color: black;")
            Episode_edit.setStyleSheet("color: black;")
            Gruppe_edit.setStyleSheet("QComboBox { color: black; }")
            Gruppe_edit.view().setStyleSheet("QComboBox QAbstractItemView { background-color: #D3D3D3; color: black;}")
            dateiendung_edit.setStyleSheet("color: black;")

            lineEdit_add_ordner_name.setStyleSheet("color: black;")

            # Setze die Größe der Textfelder so, dass sie sich horizontal ausdehnen können
            ordner_name_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            dateiname_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            comboBox_type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            dateEdit_jahr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            spinBox_staffel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            Episode_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            Gruppe_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            dateiendung_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            lineEdit_add_ordner_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


            # Alle Felder deaktivieren, außer dateiname, typ, Jahr, Staffel, Episode und Gruppe
            ordner_name_edit.setEnabled(False)
            dateiendung_edit.setEnabled(False)

            grid_layout.addWidget(ordner_name_edit, count, 0)
            grid_layout.addWidget(dateiname_edit, count, 1)
            grid_layout.addWidget(comboBox_type, count, 2)
            grid_layout.addWidget(dateEdit_jahr, count, 3)
            grid_layout.addWidget(spinBox_staffel, count, 4)
            grid_layout.addWidget(Episode_edit, count, 5)
            grid_layout.addWidget(Gruppe_edit, count, 6)
            grid_layout.addWidget(dateiendung_edit, count, 7)

            self.entry_boxes.extend([ordner_name_edit, dateiname_edit, comboBox_type, dateEdit_jahr, spinBox_staffel, Episode_edit, Gruppe_edit, dateiendung_edit])

            count += 1

        scroll_layout.addLayout(grid_layout)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        save_button = QPushButton("Speichern")
        save_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        cancel_button = QPushButton("Abbrechen und Programm beenden")
        cancel_button.setStyleSheet("background-color: red; color: white; font-weight: bold;") 
        cancel_button.clicked.connect(self.on_cancel_clicked)
        layout.addWidget(cancel_button)

        self.setLayout(layout)
        self.videofiles = videofiles

    # Funktion zum Einfügen des Dateinamens in alle Felder
    def insert_filename(self, new_filename, index):
        for i in range(index, len(self.entry_boxes), 8):
            widget = self.entry_boxes[i]
            if isinstance(widget, QLineEdit):
                widget.setText(new_filename)
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(new_filename)
            elif isinstance(widget, QDateEdit):
                widget.setDate(QtCore.QDate.fromString(new_filename, "yyyy"))
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(new_filename))

    # Funktion zum automatischen Befüllen der Episodenliste
    def fill_episodes(self, start_value):
        episode_index = 5  # Der Index der Episoden-Felder in der entry_boxes-Liste (5. Feld in jeder Zeile)
        # Iteriere über alle Episode-Felder in der entry_boxes-Liste
        for i in range(episode_index, len(self.entry_boxes), 8):
            widget = self.entry_boxes[i]
            if isinstance(widget, QLineEdit): 
                widget.setText(str(start_value))
                start_value += 1 
               
    # Funktion zum Speichern der Änderungen
    def save_changes(self):
        index = 0
        for key, value in sorted(self.videofiles.items()):
            updated_values = []
            for box in self.entry_boxes[index:index+len(value)]:
                if isinstance(box, QLineEdit):
                    updated_values.append(box.text())
                elif isinstance(box, QComboBox):
                    updated_values.append(box.currentText())
                elif isinstance(box, QDateEdit):
                    updated_values.append(box.date().toString(Qt.ISODate))
                elif isinstance(box, QSpinBox):
                    updated_values.append(str(box.value()))
            self.videofiles[key] = updated_values
            index += len(value)
        self.close()
        return self.videofiles

    def on_cancel_clicked(self):
        self.close()
        sys.exit()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)

    def open_anime_folder(self, path_ordner):
        try:
            os.startfile(path_ordner)
        except Exception as e:
            print("Fehler beim Öffnen des Ordners:", e)

  

def create_gui(videofiles, path, typ_liste, path_ordner):
    with open(path, "r+") as file:
        gruppenliste = file.read().splitlines()
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    gui = FolgenlisteGUI(videofiles, gruppenliste, typ_liste, path_ordner)
    gui.show()
    app.exec_()
    return gui.videofiles


if __name__ == "__main__":

    typ_liste = [
        'OVA','Bonus','Film','AMV','TS','ONA'
    ]

    path = r'C:\Users\admin\Desktop\Gruppen.txt'

    path_ordner = r'C:\Users\admin\Desktop\Kurenai'

    videofiles = {
    'a place to bloom.AMV-Hilary_Cullen.mp4': ['2016', 'Hilary cullen', '', '', '1', '', 'A place to bloom amv', '.mp4'],
    'A Tale of Demons Magic and Insanity.AMV-KenjiKyou.mp4': ['2017', 'A tale of demons magic and insanity ', 'AMV', '', '0', '', 'Kenjikyou', '.mp4'],
    'Absolutely save you.AMV-jinshi.mp4': ['2018', 'Absolutely save you ', 'AMV', '', '0', '', 'Jinshi', '.mp4'], 'All Alone.AMV-aias.mp4': ['2017', 'All alone ', 'AMV', '', '0', '', 'Aias', '.mp4'],
    'All that you cant leave behind.AMV-ScorpionsUltd.mp4': ['2019', 'All that you cant leave behind ', 'AMV', '', '0', '', 'Scorpionsultd', '.mp4'], 'Alone.AMV-KenjiKyou.mp4': ['2017', 'Alone ', 'AMV', '', '0', '', 'Kenjikyou', '.mp4'],
    'Angels Memories.AMV-cecco.mp4': ['2020', 'Angels memories ', 'AMV', '', '0', '', 'Cecco', '.mp4'], 'Another Day.AMV-Wormwood.avi': ['2017', 'Another day ', 'AMV', '', '0', '', 'Wormwood', '.avi'],
    'in-si-de-sa-in.AMV-zzerg.mp4': ['2021', 'In-si-de-sa-in ', 'AMV', '', '0', '', 'Zzerg', '.mp4'], 'Inner Demons.AMV-XIII.mp4': ['2017', 'Inner demons ', 'AMV', '', '0', '', 'Xiii', '.mp4'],
    'Insanity.AMV-Nurikokourin.mp4': ['2022', 'Insanity ', 'AMV', '', '0', '', 'Nurikokourin', '.mp4']
}
    


    videofiles= create_gui(videofiles, path, typ_liste, path_ordner)
    print(videofiles)
