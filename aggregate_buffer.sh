
set -e

DB_HOST="mysql_db"
DB_USER="user"
DB_PASSWORD="rootpassword"
DB_NAME="autohaus_db"
FLAG_TABLE="a_status"
COMPLETION_FLAG="complete"

while true; do

    if echo "SELECT * FROM $FLAG_TABLE WHERE status = '$COMPLETION_FLAG';" | mysql -h$DB_HOST -u$DB_USER -p$DB_PASSWORD $DB_NAME | grep -q $COMPLETION_FLAG; then
        
        break
    fi
   
    echo "Wait for Aggregation"
    sleep 30 
done


echo "Aggregation complete"
exec "$@"
