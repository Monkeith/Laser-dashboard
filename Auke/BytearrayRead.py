import psycopg2
import mysecrets

# Functie om byte-array gegevens uit de database te lezen
def read_byte_arrays():
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

        # Voer een query uit om de byte-array gegevens uit de tabel te lezen
        cur.execute("SELECT byte_array FROM bytearray_table")

        # Haal de byte-array gegevens op en geef ze weer
        byte_arrays = cur.fetchall()
        for row in byte_arrays:
            byte_array = row[0]
            byte_array_values = list(byte_array)
            print(byte_array_values)

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        # Sluit de cursor en de verbinding
        if cur:
            cur.close()
        if conn:
            conn.close()

# Roep de functie aan om byte-array gegevens uit de database te lezen
read_byte_arrays()
