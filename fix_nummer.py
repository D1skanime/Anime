
def fix_nummer(videofiles):

    SonderzeichenListe = ["/", "?", "*", "<", ">", "'", "|", ":", "[", "]"]

    for file in sorted(videofiles.keys()):
        jahr = videofiles[file][3]
        staffel = videofiles[file][4]
        episode = videofiles[file][5]
        name = videofiles[file][1]
        ordner = videofiles[file][0]

        # Prüfe, ob Jahr im Format jjjj ist, wenn nicht, mache jjjj
        if len(jahr) != 4 or not jahr.isdigit():
            jahr = '(' + jahr[:4]+')'
            videofiles[file][3] = jahr

        # Prüfe, ob Staffel = xx ist, wenn nicht, mache 0x
        if len(staffel) == 1:
            staffel = '0' + staffel
            videofiles[file][4] = staffel

        # Prüfe, ob Folge = xx oder xxx oder xxxxx usw. ist, wenn nicht, mache 0x
        if '-' not in episode and len(episode) < 3:
            episode = episode.zfill(2) 
            videofiles[file][5] = episode
        #entferne alle Leerzeichen vor dem Text und nach dem Text
            name = name.strip(' .')
            videofiles[file][1] = name
        for char in SonderzeichenListe:
            ordner = ordner.replace(char, "")
        ordner = ordner.strip(' .')
        videofiles[file][0] = ordner
 

    return videofiles                                                                                                   

if __name__ == "__main__":

    path = r'C:\Users\admin\Desktop\Gruppen.txt'

    videofiles = {
    'MM__01.mkv': ['Testffffffffffffffffffffffff  .', '  A Town Where You Live   .', 'AMV', '', '02', '01-23', 'GruppeKampfkuchen', '.mkv'],
    'MM__02.mkv': ['Test', 'A Town Where You Live.', 'Film', '2012-01-02', '2', '2', 'GruppeKampfkuchen', '.mkv'],
    'MM__03.mkv': ['Test', 'A Town Where You Live.', '', '', '0', '03', 'GruppeKampfkuchen', '.mkv'],
}

    videofiles= fix_nummer(videofiles)
    print(videofiles)