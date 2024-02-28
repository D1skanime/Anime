import os
import re
import sys

def isvideofile(daten, ordner_name, sourcelist):
    videofiles = {}
    for datei in daten:
        # Fehlerbehandlung für Dateinamen ohne Erweiterung
        try:
            dateiname, dateiendung = os.path.splitext(datei)
        except ValueError:
            continue  # Dateiname ohne Erweiterung überspringen

        if dateiendung.lower() in sourcelist:
            type = ""
            Jahr = ""
            Staffel = ""
            Episode = ""
            Gruppe = "unkekannt"
            #['Test', 'MM__01', '', '', '', '', 'unkekannt', '.mkv']
            videofiles[datei] = [ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung]  # Speichern von Ordnername, Dateiname und Dateiendung als Liste
    return videofiles

if __name__ == "__main__":
    daten = ['banner.jpg', 'clearart.png', 'extrafanart', 'extrathumbs', 'logo.png', 'MM__01-320-10.bif', 'MM__01.mkv', 'MM__01.nfo', 'MM__02-320-10.bif', 'MM__02.mkv']
    ordner_name = "Test"
    sourcelist = [".mp4", ".mkv"]
    videofiles = isvideofile(daten, ordner_name, sourcelist)
    print(videofiles)