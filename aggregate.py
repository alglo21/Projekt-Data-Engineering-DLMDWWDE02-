
import mysql.connector
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import month, year, hour, date_format, row_number, desc


spark = SparkSession.builder \
    .appName("Integration") \
    .getOrCreate()


df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/autohaus_db") \
    .option("dbtable", "umsatz") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .load()

print("Loading complete")


mon_umsatz = df.groupBy(month("Datum").alias("Monat"), year("Datum").alias("Jahr"), "Autohaus") \
    .sum("Umsatz") \
    .orderBy("Jahr", "Monat", "Autohaus")


umsatz_pro_autoverkaeufer = df.groupBy("Autohaus", "Autoverkaeufer_ID").sum("Umsatz")


zeit_umsatz = df.groupBy(hour("Uhrzeit").alias("Stunde"), date_format("Datum", 'E').alias("Wochentag"), "Autohaus") \
    .sum("Umsatz")


windowSpec = Window.partitionBy("Autohaus").orderBy(desc("sum(Umsatz)"))
top_modells = df.groupBy("Autohaus", "Modell").sum("Umsatz") \
    .withColumn("rank", row_number().over(windowSpec)) \
    .filter("rank <= 10") \
    .drop("rank")


print("Aggregation complete.")



mon_umsatz.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/autohaus_db") \
    .option("dbtable", "mon_umsatz") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

umsatz_pro_autoverkaeufer.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/autohaus_db") \
    .option("dbtable", "umsatz_pro_autoverkaeufer") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

zeit_umsatz.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/autohaus_db") \
    .option("dbtable", "zeit_umsatz") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

top_modells.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql_db:3306/autohaus_db") \
    .option("dbtable", "top_modells") \
    .option("user", "user") \
    .option("password", "rootpassword") \
    .save()

print("Export complete.")




conn = mysql.connector.connect(
    host='mysql_db',
    user='user',
    password='rootpassword',
    database='autohaus_db'
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS a_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("INSERT INTO a_status (status) VALUES ('complete')")

conn.commit()
cursor.close()
conn.close()

spark.stop()
