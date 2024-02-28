import os
import re
import sys



def find_folge_nummer(videofiles):
    for key, value in videofiles.items():
        #Sucht nach einem Muster wie "SxxExx" oder "SxxExxx"
        match = re.search(r"(.*?)(S\d{2}E\d{2,3})", value[1])
        if match:
            value[1] = match.group(1)
            # Extrahiere die Teile aus der Folgennummer
            folge_match = re.search(r"S(\d{2})E(\d{2,3})", match.group(2))
            if folge_match:
                value[4] = folge_match.group(1) # Staffelnummer
                value[5] = folge_match.group(2) # Episodennummer
        else:
            #Umkehrung des value und Suche nach einer Zahlenfolge mit mindestens zwei Ziffern und bindestrichen bei doppelfolgen
            match = re.search(r"(\d{2,}-?\d*)\D*$", value[1][::-1])
            if match:
                value[1] = value[1].replace(match.group(1)[::-1], "")
                value[5] = match.group(1)[::-1] # Episodennummer
            else:
                 # Regulärer Ausdruck, um die letzte einstellige Zahl zu extrahieren
                match = re.search(r'\b(\d)\s*$', value[1])
                if match:
                    value[1] = value[1].replace(match.group(1), "")
                    value[5] = "0" + match.group(1)
                else:
                    # Zusätzliche Überprüfung für das Muster "S1 - xx"
                    match = re.search(r"S1\s*-\s*(\d{1,2})", value[1])
                    if match:
                        value[1] = value[1].replace(match.group(1), "")
                        value[5] = match.group(1)   
    return videofiles



if __name__ == "__main__":
    videofiles =   {#ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__S01E31.mkv': ['Test', 'Maken-Ki_02v2_', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__02.mkv': ['Test', 'Naruto_026-027_ger_Sub_Uncut', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__03.mkv': ['Test', '[.h & Chinu] Koutetsujou no Kabaneri - 3', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__04.mkv': ['Test', '[[L-S] Natsume Yuujinchou S1 - 02 (1280x720 h264 AAC)[C4B217BC]', '', '', '', '', 'unkekannt', '.mkv']
                    }
    videofiles = find_folge_nummer(videofiles)
    print(videofiles)