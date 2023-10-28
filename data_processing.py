import pandas as pd
from sqlalchemy import create_engine, MetaData

# Datenbankverbindung
engine = create_engine('postgresql://myuser:mypassword@db/mydatabase')

# Pfad zur CSV-Datei
file_path = "./bitcoin_data/bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv"

# Daten in einen DataFrame laden
df = pd.read_csv(file_path)
print(df.head())

# Fehlende Werte prüfen
print(df.isnull().sum())

# Fehlende Werte durch den vorherigen Wert auffüllen (Forward Fill)
df.fillna(method='ffill', inplace=True)

# Zeitstempelspalte in ein datetime-Objekt konvertieren
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Tagesdurchschnittspreis berechnen
daily_average = df.resample('D', on='Timestamp').mean()
print(daily_average[['Open', 'Close']])

df['Price Change'] = df['Close'] - df['Open']
monthly_volatility = df.resample('M', on='Timestamp').std()['Price Change']
print(monthly_volatility)