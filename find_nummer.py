import os
import re
import sys



def find_folge_nummer(videofiles):
    for key, value in videofiles.items():
        #Sucht nach einem Muster wie "SxxExx" oder "SxxExxx" wie auch sxxexx
        match = re.search(r"(.*?)([Ss]\d{2}[Ee]\d{2,3})", value[1])
        if match:
            value[1] = match.group(1)
            # Extrahiere die Teile aus der Folgennummer
            folge_match = re.search(r"[Ss](\d{2})[Ee](\d{2,3})", match.group(2))
            if folge_match:
                value[4] = folge_match.group(1) # Staffelnummer
                value[5] = folge_match.group(2) # Episodennummer
        else:
            # Zusätzliche Überprüfung für das Muster "S1 - xx"
            match = re.search(r"S(\d)\s*-\s*(\d{1,2})", value[1])
            if match:
                value[1] = value[1].replace(match.group(0), "")
                value[4] = match.group(1)
                value[5] = match.group(2)        
            else:
                #Zahlenfolge mit mindestens zwei Ziffern und bindestrichen bei doppelfolgen
                match = re.search(r"(\d{1,3}\s*-\s*\d{1,3})", value[1])
                if match:
                    print(match)
                    value[1] = value[1].replace(match.group(0), "")
                    value[5] = match.group(1)
                else:
                    # Regulärer Ausdruck, um die letzte einstellige Zahl zu extrahieren
                    match = re.search(r'\b(\d)\s*$', value[1])
                    if match:
                        value[1] = value[1].replace(match.group(1), "")
                        value[5] = "0" + match.group(1)
                    else:
                        # Muster exxx
                        match = re.search(r"\b(e\d{1,3})\b", value[1])
                        if match:
                            print(match)
                            value[1] = value[1].replace(match.group(0), "")
                            value[5] = match.group(1)[1:]   
                           
    return videofiles



if __name__ == "__main__":
    videofiles =   {#ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__02.mkv': ['Test', 'Naruto 026-027 -hdhdh', '', '1920', '', '', 'unkekannt', '.mkv'],
                    'MM__04.mkv': ['Test', '[L-S] Natsume Yuujinchou S1 - 02', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__05.mkv': ['Test', 'dmpd-mashle magic and muscles s01e17', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__06.mkv': ['Test', 'onigiri-blue exorcist s03e05', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__07.mkv': ['Test', 'stars-boruto e224', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__08.mkv': ['Test', 'Accel World EX OVA S00E01-M-L', '', '', '', '', 'unkekannt', '.mkv']
                    }
    videofiles = find_folge_nummer(videofiles)
    print(videofiles)