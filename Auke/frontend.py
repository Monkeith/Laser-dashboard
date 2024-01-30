from dash import html, dcc, Input, Output, State, Dash
import psycopg2
import mysecrets

update_frequency = 200

app = Dash()

app.layout = html.Div([
    html.H1(id="price-ticker"),
    dcc.Interval(id="update", interval=update_frequency),
])

@app.callback(
    Output("price-ticker", "children"),
    Input("update", "n_intervals"),
)
def update_data(intervals):
    try:
        # Maak verbinding met de TimescaleDB-database
        conn = psycopg2.connect(
            dbname=mysecrets.DATABASE_NAME,
            user=mysecrets.DATABASE_USER,
            password=mysecrets.DATABASE_PASSWORD,
            host=mysecrets.DATABASE_HOST,
            port=mysecrets.DATABASE_PORT,
        )
        cursor = conn.cursor()

        # Haal de meest recente prijs op uit de database
        cursor.execute("SELECT price FROM trades ORDER BY time DESC LIMIT 1")
        latest_price_row = cursor.fetchone()
        if latest_price_row is not None:
            latest_price = latest_price_row[0]
        else:
            latest_price = "No data available"

        conn.close()

        return latest_price

    except Exception as e:
        print("Error:", e)
        return "Error fetching data"

if __name__ == '__main__':
    app.run_server(debug=True)
