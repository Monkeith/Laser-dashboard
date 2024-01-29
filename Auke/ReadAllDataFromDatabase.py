import psycopg2

# Verbindingsgegevens
dbname = "tsdb"
user = "tsdbadmin"
password = "1uG?RrmOV7x.62"
host = "ox6uce6ozv.nddn3dnk87.tsdb.cloud.timescale.com"
port = "33993"

try:
    # Maak verbinding met de database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Maak een cursor object
    cur = conn.cursor()

    # Voer een SQL-query uit om alle gegevens op te halen
    cur.execute("SELECT * FROM your_table_name;")  # Vervang your_table_name door de werkelijke naam van je tabel

    # Haal de resultaten op
    rows = cur.fetchall()

    # Print de resultaten
    for row in rows:
        print(row)

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Sluit de cursor en de verbinding
    cur.close()
    conn.close()
