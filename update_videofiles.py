import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSpinBox, QVBoxLayout, QScrollArea, QGridLayout, QLineEdit, QDateEdit, QSizePolicy, QComboBox,QHBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
from PyQt5.QtCore import QEvent
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
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        self.entry_boxes = []


        # 1. Ordnername

        lineEdit_add_ordner_name = QLineEdit()
        lineEdit_add_ordner_name.setText(videofiles[next(iter(videofiles))][0])
        lineEdit_add_ordner_name.setCursorPosition(0)
        layout.addLayout(self._row(
             "Ändere Ordnername",
            lineEdit_add_ordner_name,
            "Übernehmen",
            lambda: self.insert_filename(lineEdit_add_ordner_name.text(), 0)
))    

        # 2. Dateiname

        lineEdit_add_videofile_name = QLineEdit()
        first_key = next(iter(videofiles))
        lineEdit_add_videofile_name.setText(videofiles[first_key][1])
        lineEdit_add_videofile_name.setCursorPosition(0)
        lineEdit_add_videofile_name.setClearButtonEnabled(True)
        self._autosize_lineedit_to_text(lineEdit_add_videofile_name, cap_px=1200)
        layout.addLayout(self._row(
            "Ändere Dateiname",
            lineEdit_add_videofile_name,
            "Übernehmen",
            lambda: self.insert_filename(lineEdit_add_videofile_name.text(), 1)
        ))


        #3. Type

        comboBox_add_type = QComboBox()
        comboBox_add_type.setEditable(True)
        comboBox_add_type.addItems(typ_liste)
        comboBox_add_type.setCurrentText(videofiles[next(iter(videofiles))][2])
        comboBox_add_type.setMinimumContentsLength(12)
        comboBox_add_type.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        layout.addLayout(self._row(
            "Ändere Type",
            comboBox_add_type,
            "Übernehmen",
            lambda: self.insert_filename(comboBox_add_type.currentText(), 2)
        ))
  

        #4. Jahr
        dateEdit_add_jahr = QDateEdit()
        dateEdit_add_jahr.setDisplayFormat("yyyy")
        dateEdit_add_jahr.setCalendarPopup(False)
        dateEdit_add_jahr.setDate(QtCore.QDate.fromString(videofiles[next(iter(videofiles))][3], "yyyy"))
        dateEdit_add_jahr.setFixedWidth(100)  # klein halten
        layout.addLayout(self._row(
            "Ändere Jahr",
            dateEdit_add_jahr,
            "Übernehmen",
            lambda: self.insert_filename(dateEdit_add_jahr.date().toString("yyyy"), 3),
            expand=False
        ))

        #5. Staffel
        spinBox_add_staffel = QSpinBox()
        spinBox_add_staffel.setRange(0, 999)
        spinBox_add_staffel.setValue(int(videofiles[next(iter(videofiles))][4]))
        spinBox_add_staffel.setFixedWidth(100)

        layout.addLayout(self._row(
            "Ändere Staffelnummer",
            spinBox_add_staffel,
            "Übernehmen",
            lambda: self.insert_filename(spinBox_add_staffel.value(), 4),
            expand=False
        ))

        #6. Eingabefeld und Button für Episode-Auto-Fill
        spin_episode_start = QSpinBox()
        spin_episode_start.setRange(1, 9999)
        spin_episode_start.setValue(1)
        spin_episode_start.setFixedWidth(100)

        layout.addLayout(self._row(
            "Startwert für Episoden",
            spin_episode_start,
            "Episoden automatisch füllen",
            lambda: self.fill_episodes(spin_episode_start.value()),
            expand=False,
            btn_min_w=220
        ))


        #7. Gruppe
        comboBox_add_gruppe = QComboBox()
        comboBox_add_gruppe.setEditable(True)
        comboBox_add_gruppe.addItems(gruppenliste)
        comboBox_add_gruppe.setCurrentText(videofiles[next(iter(videofiles))][6])
        comboBox_add_gruppe.setMinimumContentsLength(12)
        comboBox_add_gruppe.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        layout.addLayout(self._row(
            "Ändere Gruppe",
            comboBox_add_gruppe,
            "Übernehmen",
            lambda: self.insert_filename(comboBox_add_gruppe.currentText(), 6)
        ))

        #Path
        dummy = QLineEdit()  # nur als Platzhalter, read-only
        dummy.setReadOnly(True)
        dummy.setPlaceholderText("Schaue in den Videodatei-Ordner")
        layout.addLayout(self._row(
            "Schauen in Ordner",
            dummy,
            "Anzeigen",
            lambda: self.open_anime_folder(path_ordner)
        ))

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
        cols = 8
        grid_row = 0
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

            grid_layout.addWidget(ordner_name_edit, grid_row, 0)
            grid_layout.addWidget(dateiname_edit, grid_row, 1)
            grid_layout.addWidget(comboBox_type, grid_row, 2)
            grid_layout.addWidget(dateEdit_jahr, grid_row, 3)
            grid_layout.addWidget(spinBox_staffel, grid_row, 4)
            grid_layout.addWidget(Episode_edit, grid_row, 5)
            grid_layout.addWidget(Gruppe_edit, grid_row, 6)
            grid_layout.addWidget(dateiendung_edit, grid_row, 7)

            orig_label = QLabel(file)  # dict-key = Originaldatei
            orig_label.setObjectName("origLabel")
            orig_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # kopierbar
            orig_label.setToolTip(file)            # Volltext beim Hover
            orig_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            orig_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self._make_elided_label(orig_label, file) # << neu: Ellipsis


            grid_layout.addWidget(orig_label, grid_row + 1, 0, 1, cols)

            self.entry_boxes.extend([ordner_name_edit, dateiname_edit, comboBox_type, dateEdit_jahr, spinBox_staffel, Episode_edit, Gruppe_edit, dateiendung_edit])

            if count % 2 == 1:
                orig_label.setProperty("rowAlt", True)
                orig_label.style().unpolish(orig_label); orig_label.style().polish(orig_label)

            grid_row += 2
            count += 1

        scroll_layout.addLayout(grid_layout)
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        self.scroll_area = scroll_area
        layout.addWidget(self.scroll_area, 1)
        self.scroll_area.setWidgetResizable(True)

        self.grid_layout = grid_layout
        QtCore.QTimer.singleShot(0, lambda: self.ensure_min_visible_rows(13))

        #Main Buttons Layout

        buttons_bar = QHBoxLayout()
        buttons_bar.addStretch(1)

        save_button = QPushButton("Speichern")
        save_button.setObjectName("primary")
        save_button.setFixedHeight(36)

        #save_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")
        save_button.clicked.connect(self.save_changes)
        #layout.addWidget(save_button)

        cancel_button = QPushButton("Abbrechen und Programm beenden")
        cancel_button.setObjectName("danger")
        cancel_button.setFixedHeight(36)
        #cancel_button.setStyleSheet("background-color: red; color: white; font-weight: bold;") 
        cancel_button.clicked.connect(self.on_cancel_clicked)
        #layout.addWidget(cancel_button)

        buttons_bar.addWidget(cancel_button)
        buttons_bar.addWidget(save_button)
        layout.addLayout(buttons_bar)

        self.setLayout(layout)
        self.videofiles = videofiles


    #Funktion für eine einheitliche Formularzeile
    def _row(self, label_text, editor, btn_text=None, btn_slot=None, expand=True, btn_min_w=None):
        h = QHBoxLayout()
        h.setSpacing(8)

        lbl = QLabel(label_text)
        lbl.setFixedWidth(170)
        lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        if expand:
            editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            editor.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        h.addWidget(lbl)
        h.addWidget(editor, 1)  # <— Editor erhält Stretch
        if btn_text:
            btn = QPushButton(btn_text)
            if btn_min_w:
                btn.setMinimumWidth(btn_min_w)
            if btn_slot:
                btn.clicked.connect(btn_slot)
            h.addWidget(btn)      # Button ohne Stretch
        return h

    def _autosize_lineedit_to_text(self, lineedit: QLineEdit, cap_px: int = 1200, padding: int = 24):
        fm = lineedit.fontMetrics()
        def adjust():
            w = fm.horizontalAdvance(lineedit.text()) + padding
            lineedit.setMinimumWidth(min(w, cap_px))
        lineedit.textChanged.connect(adjust)
        adjust()

    def _make_elided_label(self, label: QLabel, full_text: str, mode=Qt.ElideMiddle, margin_px: int = 12):
        """Hält QLabel-Text immer elidiert (…); zeigt Volltext als Tooltip."""
        label._full_text = full_text  # speichern
        def _update():
            w = max(10, label.width() - margin_px)
            label.setText(label.fontMetrics().elidedText(full_text, mode, w))
        label._elide_update = _update
        label.installEventFilter(self)
        _update()

    def eventFilter(self, obj, ev):
        # Ellipsis bei Größenänderung nachziehen
        if isinstance(obj, QLabel) and hasattr(obj, "_elide_update") and ev.type() == QEvent.Resize:
            obj._elide_update()
        # (falls du schon FocusIn->selectAll drin hast, einfach drin lassen)
        return super().eventFilter(obj, ev)      


    def ensure_min_visible_rows(self, min_rows: int = 13):
        if not self.entry_boxes:
            return
        per_row = 8
        sample = self.entry_boxes[:per_row]
        row_h = max(w.sizeHint().height() for w in sample)        # Höhe der Edit-Reihe
        label_h = self.fontMetrics().height() + 8                  # grobe Höhe der Original-Zeile
        v = self.grid_layout.verticalSpacing() or 6
        padding = 12
        per_episode = row_h + v + label_h + v
        self.scroll_area.setMinimumHeight(int(min_rows * per_episode + padding))   

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
    'a place to bloom.AMV-Hilary_Cullen.mp4': ['2016', 'Hilary cullen sehr langer Name mit viel blablablb nnnnnnnnnnn', '', '', '1', '', 'A place to bloom amv', '.mp4'],
    'A Tale of Demons Magic and Insanity.AMV-KenjiKyou.mp4': ['2017', 'A tale of demons magic and insanity ', 'AMV', '', '0', '', 'Kenjikyou', '.mp4'],
    'Absolutely save you.AMV-jinshi.mp4': ['2018', 'Absolutely save you ', 'AMV', '', '0', '', 'Jinshi', '.mp4'], 'All Alone.AMV-aias.mp4': ['2017', 'All alone ', 'AMV', '', '0', '', 'Aias', '.mp4'],
    'All that you cant leave behind.AMV-ScorpionsUltd.mp4': ['2019', 'All that you cant leave behind ', 'AMV', '', '0', '', 'Scorpionsultd', '.mp4'], 'Alone.AMV-KenjiKyou.mp4': ['2017', 'Alone ', 'AMV', '', '0', '', 'Kenjikyou', '.mp4'],
    'Angels Memories.AMV-cecco.mp4': ['2020', 'Angels memories ', 'AMV', '', '0', '', 'Cecco', '.mp4'], 'Another Day.AMV-Wormwood.avi': ['2017', 'Another day ', 'AMV', '', '0', '', 'Wormwood', '.avi'],
    'in-si-de-sa-in.AMV-zzerg.mp4': ['2021', 'In-si-de-sa-in ', 'AMV', '', '0', '', 'Zzerg', '.mp4'], 'Inner Demons.AMV-XIII.mp4': ['2017', 'Inner demons ', 'AMV', '', '0', '', 'Xiii', '.mp4'],
    'Insanity.AMV-Nurikokourin.mp4': ['2022', 'Insanity ', 'AMV', '', '0', '', 'Nurikokourin', '.mp4'],
    'A Tale of Demons Magic and Insanity.AMV-KenjiKyou.mp4': ['2017', 'A tale of demons magic and insanity ', 'AMV', '', '0', '', 'Kenjikyou', '.mp4'],
    'A Tale of Demons Magic and Insanity.AMV-KenjiKyou.mp4': ['2017', 'A tale of demons magic and insanity ', 'AMV', '', '0', '', 'Kenjikyou', '.mp4'],
    'A Tale of Demons Magic and Insanity.AMV-KenjiKyou.mp4': ['2017', 'A tale of demons magic and insanity ', 'AMV', '', '2', '', 'Kenjikyou', '.mp4'],
    'A Tale of Demons Magic and Insanity.AMV-KenjiKyou.mp4': ['2017', 'A tale of demons magic and insanity ', 'AMV', '', '0', '', 'Kenjikyou', '.mp4'],
    'A Tale of Demons Magic and Insanity.AMV-KenjiKyou.mp4': ['2017', 'A tale of demons magic and insanity ', 'AMV', '', '8', '', 'Kenjikyou', '.mp4'],
    '1 in-si-de-sa-in.AMV-zzerg.mp4': ['2021', '1 In-si-de-sa-in ', 'AMV', '', '4', '', 'Zzerg', '.mp4'],
    '2 in-si-de-sa-in.AMV-zzerg.mp4': ['2023', '2 In-si-de-sa-in ', 'AMV', '', '6', '', 'Zzerg', '.mp4'],
    '4 in-si-de-sa-in.AMV-zzerg.mp4': ['2021', '3 In-si-de-sa-in ', 'AMV', '', '2', '', 'Zzerg', '.mp4'],
    
}
    


    videofiles= create_gui(videofiles, path, typ_liste, path_ordner)
    print(videofiles)
