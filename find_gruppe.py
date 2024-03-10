import os
import re
import sys
  
def find_gruppe_in_videofile(videofiles):
    for key, value in videofiles.items():
        #Gruppennamen aus der Klammer extrahieren, falls vorhanden
        match = re.search(r'\[([^[\]]*?)\]', value[1])
        if match:
                value[1] = value[1].replace(f"[{match.group(1).strip('[]')}]", "").strip().capitalize()
                value[6] = match.group(1).strip('[]').capitalize()       
        else:
        # Hier suchen wir nach einer Zeichenkette zwischen einem Bindestrich und einem Punkt
            match = re.search(r'-(\w+)$', value[1])
            if match:
                value[1] = value[1].replace(f"-{match.group(1)}", "").strip().capitalize()
                value[6] =match.group(1).capitalize()
            else:
                 match = re.match(r'([^-]+)-(.+)', value[1])
                 if match:
                    value[1] = re.sub(fr'\b{re.escape(match.group(1))}\b', '', value[1]).strip()
                    value[6] =match.group(1).capitalize()
                    value[1] = value[1][1:].capitalize()
                
    return videofiles                 

if __name__ == "__main__":
    videofiles =   {#ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__02.mkv': ['Test', 'Naruto  -hdhdh', '', '1920', '', '026-027', 'unkekannt', '.mkv'],
                    'MM__04.mkv': ['Test', '[L-S] Natsume Yuujinchou', '', '', '1', '02', 'unkekannt', '.mkv'],
                    'MM__05.mkv': ['Test', 'dmpd-mashle magic and muscles ', '', '', '01', '17', 'unkekannt', '.mkv'],
                    'MM__06.mkv': ['Test', 'onigiri-blue exorcist ', '', '', '03', '05', 'unkekannt', '.mkv'],
                    'MM__07.mkv': ['Test', 'stars-boruto ', '', '', '', '224', 'unkekannt', '.mkv'],
                    'MM__08.mkv': ['Test', 'Accel World EX OVA ', '', '', '00', '01', 'unkekannt', '.mkv']
                    }
    videofiles = find_gruppe_in_videofile(videofiles)
    print(videofiles)