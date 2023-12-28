#Service importiert die Datensätze in die Datenbank
import csv
import mysql.connector

#Verbindung zur Datenbank herstellen
conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword'
)
cursor = conn.cursor()

print("Connection successfull")

#Falls Datenbank nicht existiert, wird eine neue erstellt 
cursor.execute("CREATE DATABASE IF NOT EXISTS autohaus_db")
cursor.execute("USE autohaus_db")

print("Database created")

#Erstellt die Tabelle für den Umsatz als Grundlage für die Aggregation 
cursor.execute("""
CREATE TABLE IF NOT EXISTS umsatz (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Autohaus VARCHAR(255),
    Datum DATE,
    Uhrzeit TIME,
    Modell VARCHAR(255),
    Autoverkaeufer_ID VARCHAR(255),
    Umsatz FLOAT
)
""")

print("Umsatz-Table created")

#CSV-Datei wird ausgelesen und die Daten in die Datenbank geladen 
path = '/app/csv_data'
for i in range(1, 6):  
    with open(f"{path}/autohaus_{i}.csv", 'r') as file:
        print(f"{path}/autohaus_{i}.csv laden.")
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            autohaus, datum, uhrzeit, modell, umsatz, autoverkaeufer_id = row
            #Ergänzung der Daten in der Umsatz-Tabelle 
            cursor.execute("INSERT INTO umsatz (Autohaus, Datum, Uhrzeit, Modell, Umsatz, Autoverkaeufer_ID) VALUES (%s, %s, %s, %s, %s, %s)",
                           (autohaus, datum, uhrzeit, modell, float(umsatz), autoverkaeufer_id))


print("CSV-Dateien geladen.")

#Tabelle zum tracken des Import-Status wird erstellt 
cursor.execute("""
CREATE TABLE IF NOT EXISTS status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

#Status "Complete" wird in der Tabelle hinzugefügt 
cursor.execute("INSERT INTO status (status) VALUES ('complete')")

#Änderungen werden commited und die Verbindung getrennt 
conn.commit()
cursor.close()
conn.close()

