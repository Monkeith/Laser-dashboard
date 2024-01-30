import psycopg2
import mysecrets
"""
Hier kun je de database mee legen zodat je nieuwe data kunt toevoegen
"""
# Verbindingsgegevens


# Functie om de volledige inhoud van een tabel te verwijderen
def truncate_table(table_name):
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

        # Voer de TRUNCATE TABLE-opdracht uit
        cur.execute(f"TRUNCATE TABLE {table_name};")

        # Commit de transactie
        conn.commit()

        print(f"Inhoud van tabel {table_name} is succesvol verwijderd.")

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        # Sluit de cursor en de verbinding
        cur.close()
        conn.close()

# Geef de naam van de tabel op die je wilt leegmaken
table_name = "bytearray_table"

# Leeg de inhoud van de tabel
truncate_table(table_name)
