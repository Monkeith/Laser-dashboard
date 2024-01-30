import psycopg2
import mysecrets
import plotly.graph_objs as go

class MultiBuffer:
    def __init__(self, buffer_size, num_subbuffers):
        self.buffer_size = buffer_size
        self.num_subbuffers = num_subbuffers
        self.buffers = [[] for _ in range(num_subbuffers)]

    def add_data(self, data):
        # Voeg nieuwe gegevens toe aan de eerste subbuffer
        self.buffers[0].append(data)

        # Als de eerste subbuffer te groot is, schuif deze door naar de volgende subbuffer
        if len(self.buffers[0]) >= self.buffer_size:
            for i in range(self.num_subbuffers - 1):
                self.buffers[i], self.buffers[i + 1] = self.buffers[i + 1], self.buffers[i]
            self.buffers[-1] = []

    def get_data(self):
        # Geef de gegevens van de laatste subbuffer terug
        return self.buffers[-1]

    def read_bytearrays_from_database(self, table_name, column_name, num_records):
        try:
            # Verbinding maken met de database
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
            cur.execute(f"SELECT {column_name} FROM {table_name} LIMIT {num_records}")

            # Haal de byte-array gegevens op en voeg ze toe aan de buffer
            byte_arrays = cur.fetchall()
            for byte_array in byte_arrays:
                self.add_data(byte_array[0])

        except psycopg2.Error as e:
            print("Error:", e)

        finally:
            # Sluit de cursor en de verbinding
            if cur:
                cur.close()
            if conn:
                conn.close()

# Maak een MultiBuffer-object en lees bytearrays uit de database
buffer_size = 100  # Grootte van elke subbuffer
num_subbuffers = 3  # Aantal subbuffers
multi_buffer = MultiBuffer(buffer_size, num_subbuffers)
multi_buffer.read_bytearrays_from_database("bytearray_table", "byte_array", 10)

# Haal de bytearrays op uit de buffer
byte_array_values = multi_buffer.get_data()

# Maak een lijngrafiek met behulp van Plotly
def create_line_chart(byte_array_values):
    return go.Figure(
        data=[
            go.Scatter(
                x=list(range(len(byte_array_values))),
                y=byte_array_values,
                mode='lines',
                name='Byte Array'
            )
        ],
        layout=go.Layout(
            title='Byte Array Grafiek',
            xaxis={'title': 'Index'},
            yaxis={'title': 'Waarde'}
        )
    )

# Weergave van de grafiek
fig = create_line_chart(byte_array_values)
fig.show()
