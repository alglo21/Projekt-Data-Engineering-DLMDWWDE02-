import pandas as pd
from sqlalchemy import create_engine, MetaData

# Datenbankverbindung
engine = create_engine('postgresql://myuser:mypassword@db/mydatabase')

