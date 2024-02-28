import os
import re
import sys

def tag_videofile(videofiles):
    num_files = len(videofiles)
    if num_files > 5:
        for key, value in videofiles.items():
            if '.AMV' in value[1]:
                value[2] = 'AMV'
            elif '.OVA' in value[1]:
                value[2] = 'OVA'
                value[4] = '0'
            elif '.TS' in value[1]:
                value[2] = 'TS'
                value[4] = '0'
            elif '.Bonus' in value[1]:
                value[2] = 'Bonus'
                value[4] = '0'    
            else: 
                value[4] = '1'  # Setze den Tag auf 'S01'
    elif num_files < 5 and num_files > 1:
        for key, value in videofiles.items():
            if '.AMV' in value[1]:
                value[2] = 'AMV'
            elif '.OVA' in value[1]:
                value[2] = 'Bonus'
                value[4] = '0'
            elif '.TS' in value[1]:
                value[2] = 'TS'
                value[4] = '0'
            elif '.Bonus' in value[1]:
                value[2] = 'OVA'
                value[4] = '0'
            else:
                value[4] = '0'    
    else:
        for key, value in videofiles.items():
            value[3] = '2000'
            value[2] = 'Film'
            value[4] = '0'
    
    return videofiles
            

if __name__ == "__main__":

    videofiles1 =   { #ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__01.mkv': ['Test', 'A Town Where You Live.S01E01-GruppeKampfkuchen', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__02.mkv': ['Test', 'Absolute Duo.S01E11-FB', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__03.mkv': ['Test', 'Antichristmas.AMV', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__04.mkv': ['Test', 'Accel World EX.OVA.S00E10-M-L', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__05.mkv': ['Test', 'Fullmetal Alchemist Specials.SP.S00E03-Gax-NTFS', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__06.mkv': ['Test', 'Amnesia OVA.Bonus.S00E01-LunaticStudio', '', '', '', '', 'unkekannt', '.mkv']
                    }
    
    videofiles1 =   { #ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__03.mkv': ['Test', 'Antichristmas.AMV', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__04.mkv': ['Test', 'Accel World EX.OVA.S00E10-M-L', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__05.mkv': ['Test', 'Fullmetal Alchemist Specials.SP.S00E03-Gax-NTFS', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__06.mkv': ['Test', 'Amnesia OVA.Bonus.S00E01-LunaticStudio', '', '', '', '', 'unkekannt', '.mkv']
                    }
    
    videofiles =   { #ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__01.mkv': ['Test', 'A Town Where You Live.S01E01-GruppeKampfkuchen', '', '', '', '', 'unkekannt', '.mkv']
                    }

    videofiles = tag_videofile(videofiles)
    print(videofiles)