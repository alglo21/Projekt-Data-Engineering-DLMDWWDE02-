# Projekt-Data-Engineering-DLMDWWDE02

Im Rahmen der Entwicklung einer batch-basierten Datenarchitektur für eine datenintensive Applikation soll zuerst ein Datensatz mit Python generiert werden, der Autohäuser, Auto-Modelle, Verkäufer und Zeitstempel umfasst und als CSV Datei gespeichert wird. Diese Daten sollen anschließend in eine MySQL-Datenbank importiert werden. Vor dem Import wird ein Skript ausgeführt das prüft, ob eine Verbindung zur Datenbank besteht und die CSV Datei erfolgreich generiert wurde. Anschließend werden die Daten mithilfe von PySpark aggregiert und verarbeitet. Hierbei sollen die Top10 Umsatzstärksten Modelle ausgewertet werden und die jeweiligen Unsätze pro Autoverkäufer ggf. noch pro Tageszeit. Die aggregierten Daten werden dann wieder zurück in die MySQL-Datenbank geschrieben. Am Ende werden die Daten noch mithilfe von Pandas visualisiert. Die Microservices sollen mithilfe von Docker containisiert werden. 

Die gewählten Komponenten erfüllen alle Anforderungen an das System (Verfügbarkeit (reliability), Skalierbarkeit (scalability) und Wartbarkeit (maintainability)), die Aufgabe ist so gut umsetzbar und wird nicht unnötig kompliziert und das Ziel der Aufgabenstellung wird vollumfänglich erreicht. 
Erste Ideen mit Datensätzen von Kaggle und dem direkten Import mithilfe der API als auch die  Verwendung einer PostgreSQL-Datenbank wurden auf Grund der Komplexität verworfen. 

# Start des Programms 

1. Docker Compose Python 3.x muss installiert werden 
2. Git clone https://github.com/alglo21/Projekt-Data-Engineering-DLMDWWDE02-
3. Lokalen Pfad wählen 
4. cd Projekt-Data-Engineering-DLMDWWDE02- 
5. docker-compose build
6. docker-compose up 

# Beenden des Programms 

1. Einfaches Beenden: docker-compose down
2. Alternativ beenden und alles löschen: docker-compose down -v

# Alternative Anpassung am Code 

Möchte man die Daten zusätzlich auf seiner lokalen Maschine speichern, muss überall wo der Pfad "data-volume:/app/csv_data" angegeben ist, zusätzlich ein lokaler Pfad angegeben werden. 
Z.b: 
volumes:
      - data-volume:/app/csv_data 
      - C:\Users\alex\Desktop\csv_data:/app/csv_data

Dieser Schritt muss sowohl in der Docker Compose Datei, als auch in allen anderen Dateien ergänzt werden, bei dem etwas auf dem Data-Volume gespeichert wird. 