
set -e

host="mysql_db"

port="3306"

until nc -z -v -w30 $host $port; do
  echo "Waiting $host:$port..."  
  sleep 10 
done

echo "$host:$port successfull"
sleep 10  
echo "Import started"

exec "$@"
