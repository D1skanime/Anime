**Anime-Episoden-Organisierer** 

Der Anime-Episoden-Organisierer ist ein Werkzeug zur Umbenennung  von Anime-Folge insbesonders Anime Fansubs. Dieses Python-Programm bietet eine grafische Benutzeroberfläche (GUI), die es Benutzern ermöglicht, ihre Episoden und Order schnell und einfach neu zu benennen.

**Funktionsweise:**

Die GUI wird mithilfe der PyQt5-Bibliothek erstellt. Diese muss auf dem System installiert werden


Der Benutzer wählt zunächst das Verzeichnis aus, das die Anime-Folgen enthält oder ein Übergeordnetes Verzeichnis das mehrere Ordner enthält.
In einem ersten Schritt werden weitere Ordner im Verzeichnis angezeigt. Die z.b von Emby und Jellyfin erstellt wurden.
Man hat die möglichkeit diese anzuschauen und zu löschen.
Dann werden alle Dateien ausser videosourcen angezeigt in einer Gui
Man hat die möglichkeit alle Typen auf einmal zu löschen oder einzlen. Es werden auch typen wie .nfo oder .bif die Emby erstellt hat angezeigt und können alle aufeinmal gelöscht werden.
Die Anwendung analysiert dann die Dateinamen, extrahiert relevante Informationen  wie Gruppenamen, die Folgen und Staffelnummer und der Type und zeigt sie in einer Liste an. Der Benutzer kann dann verschiedene Umbenennungsoptionen auswählen, wie z.B. die Anpassung von Staffalnummer, das Hinzufügen von Gruppennamen und das Zuweisen von type, Ordername, folgennamen.

Die GUI bietet eine Vorschau der vorgeschlagenen Änderungen, bevor der Benutzer die Umbenennung durchführt. Nach Bestätigung werden die ausgewählten Folgen umbenannt und die neue Ordnerstruktur wird erstellt.
Das bestehnde Verzeichniss wird auf den neuen Namen unbenannt.
Wenn es schon ein Verzeichnis mit dem Namen existiert wird der gesamte Inhalt in dieser Verzeichnis verschoben und das alte Verzeichnis gelöscht 
Die Bearbeiten Verzeichnisse werden in eine Log Datei erfasst.
Die Gruppen werden in einer Gruppen text Datei erfasst.

**Vorbedingungen:**

Um den Anime-Episoden-Organisierer auszuführen, müssen folgende Vorbedingungen erfüllt sein:

1. **Python und PyQt5:** Stellen Sie sicher, dass Python auf Ihrem System installiert ist. Installieren Sie auch die PyQt5-Bibliothek, die für die GUI verwendet wird. Sie können PyQt5 mit dem Befehl `pip install PyQt5` installieren.

2. **Befüllte oder leere Textdatei für die Gruppennamen:**
3. **Befüllte oder leere Textdatei für den Log damit das System erkennt welche Order schon bearbeitet wurden:** 

**Ausführung:**

1. Klonen oder laden Sie dieses Repository herunter.
2. Stellen Sie sicher, dass Python und PyQt5 auf Ihrem System installiert ist.
3. Führen Sie die Datei "crawler2.py" aus, indem Sie `crawler2.py` in der Kommandozeile oder im Terminal eingeben.
4. Wählen Sie das Hauptverzeichnis mit den Anime-Ordner aus.
5. Wählen Sie die Log Datei aus.
6. Wählen Sie die Gruppen Datei aus.
6. Überprüfen Sie die Vorschau der Änderungen und editieren sie wo nötig.
7. Klicken Sie auf "Speichern", um die ausgewählten Episoden umzubenennen.

Der Episoden Organisier richtet sich an alle die User die den Namen von Anisearch behalten wollen jedoch das Staffel und Episoden tagging von tvdb verwenden müssen damit die Fansubs von Emby und Jellyfin erkannt werden. Aus diesem Grund wird nach dem folgenamen.Type eingetragen
in dem Sinn Name.type.Staffe,Episode-Gruppe.
Der Type wird nur bei Bonus, OVA,Tvspezial und ONA angewendet.
