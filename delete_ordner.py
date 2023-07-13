import os
import shutil

def delete_ordner(Ordnerkill):
    Verzeichnisse_kill =  [f.path for f in os.scandir(Ordnerkill) if f.is_dir()]
    for Verzechnis_kill in Verzeichnisse_kill:
        try:
            shutil.rmtree(Verzechnis_kill)
        except OSError as e:
            print(f"Error:{e.strerror}")
    return