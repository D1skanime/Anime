import os
import shutil
import sys

def buildnew_name(videofiles):
    for file in sorted(videofiles.keys()):
        ordner_name, dateiname, typ, Jahr, Staffel, Episode, Gruppe, dateiendung = videofiles[file]
        # Überprüfung, ob Film 
        if len(Jahr) > 0 and typ == "Film":
            neue_folge_name = f"{dateiname}. {Jahr}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)
        elif len(typ) == 0:
            # Serie
            neue_folge_name = f"{dateiname}. S{Staffel}E{Episode}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)
        elif typ == "AMV":
            neue_folge_name = f"{dateiname}. {typ}.S{Staffel}E{Episode}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)    
        else:    
            neue_folge_name = f"{dateiname}. {typ} S{Staffel}E{Episode}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)
    return videofiles        

if __name__ == "__main__":
    videofiles = {
        'MM__02.mkv': ['Test(1920)', 'Naruto', 'Film', '(1920)', '00', '026-027', 'Hdhdh', '.mkv'],
        'MM__04.mkv': ['Test', 'Natsume yuujinchou', '', '', '01', '02', 'L-s', '.mkv'],
        'MM__05.mkv': ['Test', 'Mashle magic and muscles', '', '', '01', '17', 'Dmpd', '.mkv'],
        'MM__06.mkv': ['Test', 'Blue exorcist', '', '', '01', '05', 'Onigiri', '.mkv'],
        'MM__07.mkv': ['Test', 'Boruto', '', '', '01', '224', 'Stars', '.mkv'],
        'MM__08.mkv': ['Test', 'Accel World EX', 'OVA', '', '01', '01', 'unkekannt', '.mkv']
    }
    videofiles = buildnew_name(videofiles)
    print(videofiles)

