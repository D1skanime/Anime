import os
import re
import sys
  
def find_gruppe_in_videofile(videofiles):
    for key, value in videofiles.items():
        #Gruppennamen aus der Klammer extrahieren, falls vorhanden
        match = re.search(r'\[([^[\]]*?)\]', value[1])
        if match:
                value[1] = value[1].replace(f"[{match.group(1).strip('[]')}]", "").strip()
                value[6] = match.group(1).strip('[]')       
        else:
        # Hier suchen wir nach einer Zeichenkette zwischen einem Bindestrich und einem Punkt
            match = re.search(r'-(\w+)$', value[1])
            if match:
                value[1] = value[1].replace(f"-{match.group(1)}", "").strip()
                value[6] =match.group(1)
                
    return videofiles                 

if __name__ == "__main__":
    videofiles =   {#ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__03.mkv': ['Test', 'A Town Where You Live.S01E01-GruppeKampfkuchen', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__04.mkv': ['Test', '[L-S] Natsume Yuujinchou S1 - 02 (1280x720 h264 AAC)[C4B217BC]', '', '', '', '', 'unkekannt', '.mkv']
                    }
    videofiles = find_gruppe_in_videofile(videofiles)
    print(videofiles)