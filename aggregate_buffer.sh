#Bash-Skript prüft dauerhaft die Daten aggregiert wurden und führt dann das Programm fort
set -e
#Parameter setzen
DB_HOST="mysql_db"
DB_USER="user"
DB_PASSWORD="rootpassword"
DB_NAME="autohaus_db"
FLAG_TABLE="a_status"
COMPLETION_FLAG="complete"

#Endlosschleife 
while true; do
    #Suche nach Flagge in der Datenbank
    if echo "SELECT * FROM $FLAG_TABLE WHERE status = '$COMPLETION_FLAG';" | mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD $DB_NAME | grep -q $COMPLETION_FLAG; then
        #Beenden falls Flagge gefunden 
        break
    fi
   #Warten auf setzen der Flagge, dass Aggregierung erfolgreich war (30Sek)
    echo "Wait for Aggregation"
    sleep 30 
done

#Aggregation erfolgreich und Skript wird ausgeführt 
echo "Aggregation complete"
exec "$@"
