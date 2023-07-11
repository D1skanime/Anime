import os
import re

# Finde den Gruppennamen für die Folge im Verzeichnis
def finde_groupname(path, SourceList):
    Videofiles = os.listdir(path)

    for file in Videofiles:
        # Überprüfe, ob die Datei eine Videodatei ist
        if any(file.lower().endswith(ext) for ext in SourceList):
            # Extrahiere den Gruppennamen aus dem Dateinamen
            print("------------------------------------------")
            print("\n".join(Videofiles)) 
            print("\n""------------------------------------------")
            match = re.search(r"^\[([^\]]+)\]|(?<=-)[A-Za-z0-9_-]+(?=\.)", file)
            if match:
                Gruppename = match.group(0)
                return "-"+Gruppename

    return "-null"   