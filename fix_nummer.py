import re
def fix_nummer(videofiles):

    SonderzeichenListe = ["/", "?", "*", "<", ">", "'", "|", ":", "[", "]"]

    for file in sorted(videofiles.keys()):
        ordner = videofiles[file][0]
        name = videofiles[file][1]
        type_ = videofiles[file][2]
        jahr = videofiles[file][3]
        staffel = videofiles[file][4]
        episode = videofiles[file][5]
        
        # Prüfe, ob Jahr im Format jjjj ist, wenn nicht, mache jjjj
        if type_ == 'Film':
            if len(jahr) != 4 or not jahr.isdigit():
                videofiles[file][3] = '(' + jahr[:4]+')'
                videofiles[file][0] = ordner+videofiles[file][3]
        else:
            videofiles[file][3] = ''        

        # Prüfe, ob Staffel = xx ist, wenn nicht, mache 0x
        if len(staffel) == 1:
            videofiles[file][4] = '0' + staffel

        # Prüfe, ob Folge = xx oder xxx oder xxxxx usw. ist, wenn nicht, mache 0x
        if '-' not in episode and len(episode) < 3:
            videofiles[file][5] = episode.zfill(2) 
        #entferne alle Leerzeichen vor dem Text und nach dem Text
            remove_pattern_regex = '|'.join(map(re.escape, SonderzeichenListe))
            name = re.sub(remove_pattern_regex, '', name, flags=re.IGNORECASE)
            videofiles[file][1] = name.strip(' .')

            remove_pattern_regex = '|'.join(map(re.escape, SonderzeichenListe))
            ordner = re.sub(remove_pattern_regex, '', ordner, flags=re.IGNORECASE)
            videofiles[file][0] = ordner.strip(' .')
 

    return videofiles                                                                                                   

if __name__ == "__main__":

    videofiles = {
    'MM__02.mkv': ['Test', 'Naruto', 'Film', '1920-01-01', '0', '026-027', 'Hdhdh', '.mkv'],
    'MM__04.mkv': ['Test', 'Natsume yuujinchou', '', '2000-01-01', '1', '02', 'L-s', '.mkv'],
    'MM__05.mkv': ['Test', 'Mashle magic and muscles', '', '2000-01-01', '1', '17', 'Dmpd', '.mkv'],
    'MM__06.mkv': ['Test', 'Blue exorcist', '', '2000-01-01', '1', '05', 'Onigiri', '.mkv'],
    'MM__07.mkv': ['Test', 'Boruto', '', '2000-01-01', '1', '224', 'Stars', '.mkv'],
    'MM__08.mkv': ['Test', 'Accel World EX  ', 'OVA', '2000-01-01', '1', '01', 'unkekannt', '.mkv']
}

    videofiles= fix_nummer(videofiles)
    print(videofiles)