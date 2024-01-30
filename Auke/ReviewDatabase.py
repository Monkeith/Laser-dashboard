import psycopg2
import mysecrets

try:
    # Maak verbinding met de database
    conn = psycopg2.connect(
        dbname=mysecrets.DATABASE_NAME,
        user=mysecrets.DATABASE_USER,
        password=mysecrets.DATABASE_PASSWORD,
        host=mysecrets.DATABASE_HOST,
        port=mysecrets.DATABASE_PORT,
    )

    # Maak een cursor object
    cur = conn.cursor()

    # Voer een SQL-query uit om alleen de laatste rij op te halen
    cur.execute("SELECT * FROM your_table_name ORDER BY timestamp_column DESC LIMIT 1;")  # Vervang your_table_name door de werkelijke naam van je tabel

    # Haal de resultaten op
    row = cur.fetchone()

    # Print de resultaten
    if row:
        print(row)
    else:
        print("Geen gegevens gevonden.")

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Sluit de cursor en de verbinding
    cur.close()
    conn.close()
