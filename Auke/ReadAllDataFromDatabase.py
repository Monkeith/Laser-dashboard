import psycopg2
import mysecrets

# Verbindingsgegevens


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

    # Voer een SQL-query uit om alle gegevens op te halen
    cur.execute("SELECT * FROM trades;")  # Vervang your_table_name door de werkelijke naam van je tabel

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
