# dhbw-ki-astern

![PythonVersion][python-image]
![CodeInspectionScore][code-inspection-score]
![CodeInspectionStatus][code-inspection-status]

> Eine Konsolenanwendung, welche mithilfe des A*-Algorithmus den schnellsten Weg zur Koordinationszentrale im Borg-Kubus 
> zeigt. Beim Erstellen dieser Anwendung wurden keine Robotor verletzt. :robot:

## Verwendung

### Start-Command

Die Anwendung kann mit 

```shell script
python main.py -i IMPORT_PATH
```
gestartet werden. Der vorgegebene Datensatz liegt in `resources/data.csv`. 

Eine vollständige Übersicht über alle Parameter bietet die Help-Message:
```shell script
python main.py -h
```

Es können drei verschiedene Log-Level gesetzt werden:

1. Silent (kein Parameter): Keine Ausgabe in der Konsole
2. Verbose (`[-v]`): Gibt Info-Nachrichten während des Ablaufs aus
3. Debug (`[-d]`): Gibt detailierte interne Nachrichten beim Import und Algorithmus aus (Genauer Pfad, Kosten etc.)

### Validation Tests

Validation Tests validieren die korrekte Arbeitsweise des Algorithmus. Sie können im Project-Root mit dem Befehl

```shell script
python -m unittest discover -s ./validation -p "*_validate.py" -v
```

gestartet werden.

## Changelog
### v0.1
Implementiert:
- main.py mit argparser
- FileController für Datenimport
- Resourcen hinzugefügt

### v0.2
Implementiert:
- AStarController für Algorithmus
- docs für Dokumentation
- Code Inspector für statische Code-Analyse

### v0.2.1
Geändert:
- Code-Violations entfernt
- Logging verbessert
- Technische Dokumentation in separate PDF verschoben
- README.md Verschlimmbesserungen

### v0.3
Implementiert:
- Validation Tests für Algorithmus
- Zeitmessung für Algorithmus

Geändert:
- Weitere Violations entfernt (Coding Conventions, Naming Conventions)
- Codekommentare verbessert

<!--Image Resources-->
[python-image]: https://img.shields.io/badge/python-v3.8.5+-blue?logo=python
[code-inspection-score]: https://www.code-inspector.com/project/16904/score/svg
[code-inspection-status]: https://www.code-inspector.com/project/16904/status/svg
