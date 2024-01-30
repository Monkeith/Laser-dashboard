import asyncio
import psycopg2
import mysecrets
from websockets import connect

# Maak verbinding met de TimescaleDB-database
conn = psycopg2.connect(
    dbname=mysecrets.DATABASE_NAME,
    user=mysecrets.DATABASE_USER,
    password=mysecrets.DATABASE_PASSWORD,
    host=mysecrets.DATABASE_HOST,
    port=mysecrets.DATABASE_PORT,
)
cursor = conn.cursor()

# Creëer de tabel in TimescaleDB
cursor.execute("DROP TABLE IF EXISTS audio")
cursor.execute("""CREATE TABLE audio(
                    frequentie FLOAT
                    )""")
conn.commit()

# Verbinding nodig met esp32
url = "url van de esp32"

async def save_down(url):
    trades_buffer = []
    async with connect(url) as websocket:
        while True:
            data = await websocket.recv()
            trades_buffer.append((data,))
            if len(trades_buffer) >= 10:  # Verander 10 naar het gewenste aantal items in de buffer
                print("Writing to db")
                cursor.executemany("INSERT INTO audio (frequentie) VALUES (%s)", trades_buffer)
                conn.commit()
                trades_buffer = []  # Leeg de buffer

asyncio.run(save_down(url))
