
set -e

host="mysql_db"

port="3306"

until nc -z -v -w30 $host $port; do
  echo "Waiting..."  
  sleep 10 
done

echo "Successfull"
sleep 10  
echo "Import started"

exec "$@"
