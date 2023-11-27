
import csv
import random
import datetime
import os



autohaus_anzahl = 5  
tage = 91   
modell_anzahl = 20    
autoverkaeufer_pro_autohaus = 5   
datensatz_gesamt = 1000000  

volume_csv_directory = '/app/csv_data'
desktop_directory = '/app/csv_data_desktop'
os.makedirs(volume_csv_directory, exist_ok=True)
os.makedirs(desktop_directory, exist_ok=True)

def random_modellnummer():
  
    return ["Modell" + ''.join(random.choice("0123456789") for _ in range(9)) for _ in range(modell_anzahl)]

def random_uhrzeit():
   
    return datetime.time(random.randint(8, 19), random.randint(0, 59))

def autoverkaeufer_ids():
    
    return ["ID" + ''.join(random.choice("0123456789") for _ in range(8)) for _ in range(autoverkaeufer_pro_autohaus)]

modell_liste = random_modellnummer()
autohaeuser = [f"Autohaus {i + 1}" for i in range(autohaus_anzahl)]
end_datum = datetime.datetime.now().date()
start_datum = end_datum - datetime.timedelta(days=tage - 1)
datensaetze_pro_autohaus = datensatz_gesamt // autohaus_anzahl 
datensaetze_pro_tag = datensaetze_pro_autohaus // tage  

for i, autohaus in enumerate(autohaeuser):
    autoverkaeufer = autoverkaeufer_ids()
    datei_name = f"autohaus_{i + 1}.csv"

    for j in range(tage):
        aktuelles_datum = start_datum + datetime.timedelta(days=j)
        autohaus_datensaetze = []

        
        for modell in modell_liste:
            for _ in range(20):
                umsatz = round(random.uniform(10000, 50000), 2) 
                zeit = random_uhrzeit()  
                autoverkaeufer = random.choice(autoverkaeufer) 
                autohaus_datensaetze.append([aktuelles_datum, zeit, autohaus, modell, umsatz, autoverkaeufer])

        
        while len(autohaus_datensaetze) < datensaetze_pro_tag:
            modell = random.choice(modell_liste)
            umsatz = round(random.uniform(10000, 50000), 2)
            zeit = random_uhrzeit()
            autoverkaeufer = random.choice(autoverkaeufer)
            autohaus_datensaetze.append([aktuelles_datum, zeit, autohaus, modell, umsatz, autoverkaeufer])

        try:
           
            with open(os.path.join(volume_csv_directory, datei_name), mode='a', newline='') as datei:
                writer = csv.writer(datei)
                if i == 0:  
                    writer.writerow(["Autohaus", "Datum", "Uhrzeit","Modell", "Umsatz", "Autoverkäufer-ID"])
                for datensatz in autohaus_datensaetze:
                    writer.writerow(datensatz)

           
            with open(os.path.join(desktop_directory, datei_name), mode='a', newline='') as datei:
                writer = csv.writer(datei)
                if i == 0:  
                    writer.writerow(["Autohaus", "Datum", "Uhrzeit", "Modell", "Umsatz", "Autoverkäufer-ID"])
                for datensatz in autohaus_datensaetze:
                    writer.writerow(datensatz)
        except Exception as e:
            print(f"Fehler: Datei kann nicht geschrieben werden {datei_name}: {e}")

print(f"{datensatz_gesamt} CSV erfolgreich erstellt")  
