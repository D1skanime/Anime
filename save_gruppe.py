import os
import re
import sys

def save_gruppe(path, videofiles):

    geschriebene_gruppen = []

    with open(path, "r+") as file:
        geschriebene_gruppen = file.read().splitlines()
    with open(path, "a") as file_text:    
        for key in sorted(videofiles.keys()):
            gruppe = videofiles[key][6]
            if gruppe not in geschriebene_gruppen:
                file_text.write("\n" + gruppe)
                geschriebene_gruppen.append(gruppe)


if __name__ == "__main__":
    path = r"C:\Users\admin\Desktop\Gruppen.txt"
    videofiles = {
        'A Town Where You Live.Bonus.S01E01-GruppeKampfkuchen.mkv': ['test3', 'A Town Where You Live', 'AMV', '', '02', '01-23', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E01-GruppeKampfkuchen.mkv'],
        'MM__02.mkv': ['Test', 'A Town Where You Live', 'Film', '2012', '02', '02', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E02-GruppeKampfkuchen.mkv'],
        'MM__03.mkv': ['Test', 'A Town Where You Live', '', '', '00', '03', 'GruppeKampfkuchen', '.mkv','A Town Where You Live.Bonus.S01E03-GruppeKampfkuchen.mkv']
    }

    save_gruppe(path, videofiles)