import psycopg2
import random
import time
import secrets

# SQL-opdracht om tabel te maken
create_table_query = """
CREATE TABLE IF NOT EXISTS your_table_name (
    timestamp_column TIMESTAMP,
    sound_level INTEGER
);
"""

try:
    # Maak verbinding met de database
    conn = psycopg2.connect(
        dbname=secrets.DATABASE_NAME,
        user=secrets.DATABASE_USER,
        password=secrets.DATABASE_PASSWORD,
        host=secrets.DATABASE_HOST,
        port=secrets.DATABASE_PORT,
    )

    # Maak een cursor object
    cur = conn.cursor()

    # Voer de CREATE TABLE-opdracht uit
    cur.execute(create_table_query)

    while True:
        # Genereer een willekeurig getal tussen 100 en 1000
        sound_level = random.randint(100, 1000)

        # Krijg de huidige tijdstempel
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # Voeg de gegevens toe aan de tabel
        cur.execute("""
            INSERT INTO your_table_name (timestamp_column, sound_level)
            VALUES (%s, %s);
        """, (timestamp, sound_level))

        # Commit de transactie
        conn.commit()

        print("Data toegevoegd aan de database:", timestamp, sound_level)

        time.sleep(0.01)  # Wacht 1 seconde voordat je het volgende willekeurige getal toevoegt

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Sluit de cursor en de verbinding
    cur.close()
    conn.close()
