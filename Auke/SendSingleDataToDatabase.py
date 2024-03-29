import psycopg2
import mysecrets

# SQL-opdracht om tabel te maken
create_table_query = """
CREATE TABLE IF NOT EXISTS your_table_name (
    timestamp_column TIMESTAMP,
    sound_level INTEGER
);
"""
#Table name

your_table_name = Bytearray_table
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
        dbname=mysecrets.DATABASE_NAME,
        user=mysecrets.DATABASE_USER,
        password=mysecrets.DATABASE_PASSWORD,
        host=mysecrets.DATABASE_HOST,
        port=mysecrets.DATABASE_PORT,
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
