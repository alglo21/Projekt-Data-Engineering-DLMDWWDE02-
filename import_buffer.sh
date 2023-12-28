#Bash-Skript prüft dauerhaft die Datenbank und führt dann das Programm fort
set -e

DB_HOST="mysql_db"
DB_USER="user"
DB_PASSWORD="rootpassword"
DB_NAME="autohaus_db"
FLAG_TABLE="status"
COMPLETION_FLAG="complete"

#Endlosschleife
while true; do
    #Suche nach Flagge in der Datenbank
    if echo "SELECT * FROM $FLAG_TABLE WHERE status = '$COMPLETION_FLAG';" | mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD $DB_NAME | grep -q $COMPLETION_FLAG; then
      #Beenden falls Flagge gefunden 
        break
    fi
   #Warten auf setzen der Flagge, dass Import erfolgreich war (30Sek)
    echo "Waiting for Import"
    sleep 30  
done

#Import erfolgreich und Skript wird ausgeführt 
echo "Import successfull"
exec "$@"
