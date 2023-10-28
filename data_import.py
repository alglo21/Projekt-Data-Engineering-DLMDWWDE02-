import kaggle
import os
from sqlalchemy import create_engine, MetaData

# Kaggle API konfigurieren
kaggle.api.authenticate()
kaggle_api_key_path = "C:\Users\glohs\mein_projekt"
os.environ["KAGGLE_CONFIG_DIR"] = os.path.dirname(kaggle_api_key_path)

# Datenbankverbindung
DATABASE_URL = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
engine = create_engine(DATABASE_URL)

# Daten von Kaggle herunterladen
dataset_name = "mczielinski/bitcoin-historical-data"
download_path = "./bitcoin_data"

if not os.path.exists(download_path):
    os.makedirs(download_path)

kaggle.api.dataset_download_files(dataset_name, path=download_path, unzip=True)
