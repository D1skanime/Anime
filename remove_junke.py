import os
import re
import sys


def remove_junke(videofiles):
    for key, value in videofiles.items():
        # Alles nach eckigen Klammern entfernen, aber die Klammern am Anfang stehen lassen
        value[1] = re.sub(r'(?<!^)\[.*?\]', '', value[1])
        # Alles zwischen runden Klammern matchen
        matches = re.findall(r'\((.*?)\)', value[1])
        if matches:
            for match in matches:
                # Prüfen, ob das Match genau 4 Zahlen enthält um das Jahr zu speichern
                if re.match(r'^\d{4}$', match):
                    value[3] = match
                    value[1] = value[1].replace(f'({match})', '').strip()   
                else:
                    # Ersetzen Sie das gefundene Muster mit Klammern im Ersatzmuster
                    value[1] = re.sub(f'\s*\({match}\)', '', value[1]).strip()
        # Entfernen spezifischer Muster (unabhängig von der Groß- und Kleinschreibung)
        remove_patterns = ['ger_Sub_', 'uncut', '.1080p', '.aac', '.web-dl', '.x264', 'folge', 'season']
        for pattern in remove_patterns:
            value[1] = re.sub(re.escape(pattern), '', value[1], flags=re.IGNORECASE)            
        #entferne alle _ mit ""
        value[1] = value[1].replace('_', ' ')             
    return videofiles


if __name__ == "__main__":
    videofiles =   {#ordner_name, dateiname, type, Jahr, Staffel, Episode, Gruppe, dateiendung
                    'MM__02.mkv': ['Test', 'Naruto_026-027_ger_Sub_Uncut(1920)(fjjff1575)-hdhdh[ghhjghji][4545fdfsd]', '', '', '', '', 'unkekannt', '.mkv'],
                    'MM__04.mkv': ['Test', '[L-S] Natsume Yuujinchou S1 - 02.x264 (1280x720 h264 AAC)[C4B217BC].1080P_.aac-SNK', '', '', '', '', 'unkekannt', '.mkv']
                    }
    videofiles = remove_junke(videofiles)
    print(videofiles)