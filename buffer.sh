#Skript prüft ob eine Verbindung zur Datenbank hergestellt werden konnte 
set -e

host="mysql_db"

port="3306"

#Verbindung wird erstellt 

until nc -z -v -w30 $host $port; do

#Warten auf Verbindung, probiert alle 10sek erneut 
  echo "Waiting..."  
  sleep 10 
done

#Verbindung erfolgreich und Import Skript wird gestartet 
echo "Successfull"
sleep 10  
echo "Import started"

exec "$@"
