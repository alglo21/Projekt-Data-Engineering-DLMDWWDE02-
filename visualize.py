#Service zur Visualisierung der aggregierten Daten. Abhängigkeit zum Aggregation-Service
#Pandas wird zur Visualisierung genutzt
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd

#Verbindung zur Datenbank herstellen
def establish_connection():
    return mysql.connector.connect(
        host='mysql_db',
        user='user',
        password='rootpassword',
        database='autohaus_db'
    )


volume_directory = '/app/csv_data'

#Service lädt die Daten aus der Datenbank und konvertiert diese 
def fetch_data(query, connection):
    return pd.read_sql(query, connection)

#Erstellt die Visualisierung der aggregierten Daten für den Umsatz
def mon_umsatz_pro_autohaus(connection):
   
    mon_umsatz_query = """
    SELECT Monat, Autohaus, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM mon_umsatz
    GROUP BY Monat, Autohaus
    """
   #Pivottabelle
    mon_umsatz = fetch_data(mon_umsatz_query, connection)
    pivot_mon_umsatz = mon_umsatz.pivot(index='Monat', columns='Autohaus', values='Gesamtumsatz')
    
    #Balkendiagramm 
    pivot_mon_umsatz.plot(kind='bar', figsize=(15, 7))
    plt.ylim([pivot_mon_umsatz.values.min()-10000, pivot_mon_umsatz.values.max()+100000]) 
    plt.title('Monatlicher Gesamtumsatz pro Autohaus')
    plt.ylabel('Umsatz')
    plt.tight_layout()

    #Visualisierung als PNG-Datei speichern 
    plt.savefig(f"{volume_directory}/mon_umsatz.png")  
    plt.close()

#Erstellt die Visualisierung der aggregierten Daten für den Umsatz pro Verkäufer 
def umsatz_pro_autoverkaeufer(connection):
    autoverkaeufer_umsatz_query = """
    SELECT Autoverkaeufer_ID, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM umsatz_pro_autoverkaeufer
    GROUP BY Autoverkaeufer_ID
    """
    autoverkaeufer_umsatz = fetch_data(autoverkaeufer_umsatz_query, connection)
    autoverkaeufer_umsatz = autoverkaeufer_umsatz.sort_values(by='Gesamtumsatz', ascending=False)
    autoverkaeufer_umsatz.plot(x='Autoverkaeufer_ID', y='Gesamtumsatz', kind='bar', figsize=(15, 7))
    plt.ylim([autoverkaeufer_umsatz['Gesamtumsatz'].min()-10000, autoverkaeufer_umsatz['Gesamtumsatz'].max()+100000])
    plt.title('Umsatz pro Autoverkaeufer in allen Autohäusern')
    plt.ylabel('Umsatz')
    plt.tight_layout()

    #Visualisierung als PNG-Datei speichern 
    plt.savefig(f"{volume_directory}/autoverkaeufer_umsatz.png")
    plt.close()

#Erstellt die Visualisierung der aggregierten Daten für den Umsatz pro Tageszeit 
def zeit_umsatz(connection):
    zeit_umsatz_query = """
    SELECT Stunde, Autohaus, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM zeit_umsatz
    GROUP BY Stunde, Autohaus
    """
    zeit_umsatz = fetch_data(zeit_umsatz_query, connection)
    pivot_zeit_umsatz = zeit_umsatz.pivot(index='Stunde', columns='Autohaus', values='Gesamtumsatz')
    pivot_zeit_umsatz.plot(kind='area', stacked=True, figsize=(15, 7))
    plt.title('Umsatz pro Tageszeit')
    plt.ylabel('Umsatz')
    plt.xlabel('Stunde')
    plt.tight_layout()

    #Visualisierung als PNG-Datei speichern 
    plt.savefig(f"{volume_directory}/zeit_umsatz.png")
    plt.close()


#Erstellt die Visualisierung der aggregierten Daten für die 10 umsatzstärksten Modelle 
def top_10_modelle_alle_autohaeuser(connection):
    top_modells_query = """
    SELECT Modell, Autohaus, SUM(`sum(Umsatz)`) as Gesamtumsatz
    FROM top_modells
    GROUP BY Modelle, Autohaus
    ORDER BY Gesamtumsatz DESC
    """
  #Pivottabelle filtert 10 besten Modelle 
    top_modells = fetch_data(top_modells_query, connection)
    top_10_modells = top_modells.groupby('Modell').Gesamtumsatz.sum().nlargest(10).index.tolist()
    filtered_top_modells = top_modells[top_modells['Modell'].isin(top_10_modells)]
    pivot_top_modells = filtered_top_modells.pivot(index='Modell', columns='Autohaus', values='Gesamtumsatz')

    #Pivottabelle sortiert 
    sorted_modells = pivot_top_modells.sum(axis=1).sort_values(ascending=False).index
    pivot_top_modells = pivot_top_modells.loc[sorted_modells]

    pivot_top_modells.plot(kind='bar', stacked=True, figsize=(15, 7))
    plt.title('Top 10 Modelle aller Autohäuser')
    plt.ylabel('Umsatz')
    plt.tight_layout()

    #Visualisierung als PNG-Datei speichern 
    plt.savefig(f"{volume_directory}/top_modells.png")
    plt.close()




#Hauptfunktion 
def main():
    connection = establish_connection()
    mon_umsatz_pro_autohaus(connection)
    umsatz_pro_autoverkaeufer(connection)
    zeit_umsatz(connection)
    top_10_modelle_alle_autohaeuser(connection)
    connection.close()
    

