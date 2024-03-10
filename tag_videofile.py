import os
import re
import sys

def tag_videofile(videofiles, types):
    num_files = len(videofiles)
    if num_files > 5:
        for key, value in videofiles.items():
            for type_ in types:
                # Überprüfe, ob das gesuchte Muster ein separates Wort ist
                if re.search(fr'\b{re.escape(type_)}\b', value[1], re.IGNORECASE):
                    regex = re.compile(re.escape(type_), re.IGNORECASE)
                    value[1]= regex.sub(lambda match: '' if match.group(0).isupper() else ''.lower(), value[1])
                    value[2] = type_
                    value[4] = '0'   
            else:
                if value[3]:
                    value[2] = 'Film'
                    value[4] = '0'
                else:
                    if value[4]:
                        '' 
                    else:
                        value[4] = '1'  # Setze den Tag auf 'S01'

    elif num_files == 5 and num_files > 1:
        for key, value in videofiles.items():
            for type_ in types:
                if re.search(fr'\b{re.escape(type_)}\b', value[1], re.IGNORECASE):
                    regex = re.compile(re.escape(type_), re.IGNORECASE)
                    value[1]= regex.sub(lambda match: '' if match.group(0).isupper() else ''.lower(), value[1])
                    value[2] = type_
                    value[4] = '0'   
            else: 
                if value[3]:
                    value[2] = 'Film'
                    value[4] = '0'
                else:
                    if value[4]:
                        ''
                    else:
                        value[4] = '1'  # Setze den Tag auf 'S01''
    else:
        for key, value in videofiles.items():
            for type_ in types:
                if re.search(fr'\b{re.escape(type_)}\b', value[1], re.IGNORECASE):
                    regex = re.compile(re.escape(type_), re.IGNORECASE)
                    value[1]= regex.sub(lambda match: '' if match.group(0).isupper() else ''.lower(), value[1])
                    value[2] = type_
                    value[4] = '0'   
            else: 
                if value[3]:
                    value[2] = 'Film'
                    value[4] = '0'
                else:
                    value[3] = '2000'
                    value[2] = 'Film'
                    value[4] = '0'                     
            
    return videofiles
            

if __name__ == "__main__":

    types = ['AMV','OVA','BONUS','TS','WEB','ONA',]
  
    videofiles =   { #ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__02.mkv': ['Test', 'Naruto', '', '1920', '', '026-027', 'Hdhdh', '.mkv'],
                    'MM__04.mkv': ['Test', 'Natsume yuujinchou', '', '', '1', '02', 'L-s', '.mkv'],
                    'MM__05.mkv': ['Test', 'Mashle magic and muscles', '', '', '01', '17', 'Dmpd', '.mkv'],
                    'MM__06.mkv': ['Test', 'Blue exorcist', '', '', '03', '05', 'Onigiri', '.mkv'],
                    'MM__07.mkv': ['Test', 'Boruto', '', '', '', '224', 'Stars', '.mkv'],
                    'MM__08.mkv': ['Test', 'Accel World EX OVA ', '', '', '00', '01', 'unkekannt', '.mkv']
                    }
    
    videofiles1 =   { #ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__01.mkv': ['Test', 'A Town Where You Live.S01E01-GruppeKampfkuchen', '', '', '', '', 'unkekannt', '.mkv']
                    }
    
    videofiles3 =   { #ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__02.mkv': ['Test', 'Naruto', '', '1920', '', '026-027', 'Hdhdh', '.mkv'],
                    'MM__04.mkv': ['Test', 'Natsume yuujinchou', '', '', '1', '02', 'L-s', '.mkv'],
                    'MM__05.mkv': ['Test', 'Mashle magic and muscles Bonus', '', '', '01', '17', 'Dmpd', '.mkv'],
                    'MM__08.mkv': ['Test', 'Accel World EX OVA ', '', '', '00', '01', 'unkekannt', '.mkv']
                    }

    videofiles = tag_videofile(videofiles, types)
    print(videofiles)