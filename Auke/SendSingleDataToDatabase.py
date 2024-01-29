import psycopg2
import secrets

# SQL-opdracht om tabel te maken
create_table_query = """
CREATE TABLE IF NOT EXISTS your_table_name (
    timestamp_column TIMESTAMP,
    sound_level INTEGER
);
"""

# Voorbeeld gegevens om toe te voegen
data_to_insert = [
    ("2024-01-01 13:20:00", 100),

    # Voeg meer gegevens toe zoals gewenst
]

conn = None
cur = None

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

    # Voeg de gegevens toe aan de tabel
    for timestamp, sound_level in data_to_insert:
        cur.execute("""
            INSERT INTO your_table_name (timestamp_column, sound_level)
            VALUES (%s, %s);
        """, (timestamp, sound_level))

    # Commit de transactie
    conn.commit()

    print("Data is succesvol toegevoegd aan de database.")

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Sluit de cursor en de verbinding
    if cur:
        cur.close()
    if conn:
        conn.close()
