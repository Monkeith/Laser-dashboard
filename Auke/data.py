import asyncio
import json
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
cursor.execute("DROP TABLE IF EXISTS trades")
cursor.execute("""CREATE TABLE trades(
                    id SERIAL PRIMARY KEY, 
                    time FLOAT,
                    quantity FLOAT,
                    price FLOAT)""")
cursor.execute("CREATE INDEX IF NOT EXISTS index_time ON trades(time)")
conn.commit()

# Verbinding nodig met esp32
url = "wss://stream.binance.com:9443/ws/btcusdt@aggTrade"

async def save_down(url):
    trades_buffer = []
    async with connect(url) as websocket:
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            trades_buffer.append((data['T'], data['q'], data['p']))
            print(data)
            if len(trades_buffer) > 10:
                print("Writing to db")
                cursor.executemany("""INSERT INTO trades (time, quantity, price) VALUES (%s, %s, %s)""", trades_buffer)
                conn.commit()
                trades_buffer = []

asyncio.run(save_down(url))
