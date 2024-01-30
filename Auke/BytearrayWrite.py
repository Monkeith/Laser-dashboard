import psycopg2
import mysecrets

# SQL-opdracht om tabel te maken
create_table_query = """
CREATE TABLE IF NOT EXISTS bytearray_table (
    id SERIAL PRIMARY KEY,
    byte_array BYTEA
);
"""

# Voorbeeld gegevens om toe te voegen
data_to_insert = [
    (b'9'),

    # Voeg meer byte-array gegevens toe zoals gewenst
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
    for byte_array in data_to_insert:
        cur.execute("""
            INSERT INTO bytearray_table (byte_array)
            VALUES (%s);
        """, (byte_array,))

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
