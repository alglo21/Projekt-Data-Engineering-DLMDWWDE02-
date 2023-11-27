
import csv
import mysql.connector


conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword'
)
cursor = conn.cursor()

print("Connection successfull")


cursor.execute("CREATE DATABASE IF NOT EXISTS autohaus_db")
cursor.execute("USE autohaus_db")

print("Database created")

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


path = '/app/csv_data'
for i in range(1, 6):  
    with open(f"{path}/autohaus_{i}.csv", 'r') as file:
        print(f"{path}/autohaus_{i}.csv laden.")
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            autohaus, datum, uhrzeit, modell, umsatz, autoverkaeufer_id = row
            
            cursor.execute("INSERT INTO umsatz (Autohaus, Datum, Uhrzeit, Modell, Umsatz, Autoverkaeufer_ID) VALUES (%s, %s, %s, %s, %s, %s)",
                           (autohaus, datum, uhrzeit, modell, float(umsatz), autoverkaeufer_id))


print("CSV-Dateien geladen.")

cursor.execute("""
CREATE TABLE IF NOT EXISTS status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("INSERT INTO status (status) VALUES ('complete')")


conn.commit()
cursor.close()
conn.close()

