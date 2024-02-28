import os
import shutil
import sys

def buildnew_name(videofiles):
    for file in sorted(videofiles.keys()):
        ordner_name, dateiname, typ, Jahr, Staffel, Episode, Gruppe, dateiendung = videofiles[file]
        # Überprüfung, ob Film 
        if len(Jahr) > 0 and typ == "Film":
            neue_folge_name = f"{dateiname}.{Jahr}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)
        elif len(typ) == 0:
            # Serie
            neue_folge_name = f"{dateiname}.S{Staffel}E{Episode}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)
        elif typ == "AMV":
            neue_folge_name = f"{dateiname}.{typ}.E{Episode}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)    
        else:    
            neue_folge_name = f"{dateiname}.{typ}.S{Staffel}E{Episode}-{Gruppe}{dateiendung}"
            videofiles[file].append(neue_folge_name)
    return videofiles        

if __name__ == "__main__":
    gruppenliste = ['aaa', 'bbbb', 'cc']
    videofiles = {
        'MM__01.mkv': ['Testffffffffffffffffffffffff', 'A Town Where You Live', 'AMV', '', '02', '01-23', 'GruppeKampfkuchen', '.mkv'],
        'MM__02.mkv': ['Test', 'A Town Where You Live', 'Film', '2012', '02', '02', 'GruppeKampfkuchen', '.mkv'],
        'MM__03.mkv': ['Test', 'A Town Where You Live', '', '', '00', '03', 'GruppeKampfkuchen', '.mkv'],
        'MM__04.mkv': ['Test', 'A Town Where You Live', 'Bonus', '', '00', '03', 'GruppeKampfkuchen', '.mkv']
    }
    videofiles = buildnew_name(videofiles)
    print(videofiles)

