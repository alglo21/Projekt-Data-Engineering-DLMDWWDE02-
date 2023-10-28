import kaggle
from sqlalchemy import create_engine, MetaData

# Kaggle API konfigurieren
kaggle.api.authenticate()

# Datenbankverbindung
DATABASE_URL = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
engine = create_engine(DATABASE_URL)

# Daten von Kaggle herunterladen
kaggle.api.dataset_download_files('heptapod/titanic', file_name='train.csv', path='./data', unzip=True)

