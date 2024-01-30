import dash
from dash import State, Input, Output, html, dcc
import dash_bootstrap_components as dbc
import psycopg2
import mysecrets

update_frequency = 200

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


# Functie om de frequentie op te halen uit de database
def get_latest_frequency():
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

        # Haal de meest recente frequentie op uit de database
        cursor.execute("SELECT frequentie FROM audio LIMIT 1")

        latest_frequency_row = cursor.fetchone()
        if latest_frequency_row is not None:
            latest_frequency = latest_frequency_row[0]
        else:
            latest_frequency = "No data available"

        conn.close()

        return latest_frequency

    except Exception as e:
        print("Error:", e)
        return "Error fetching data"


# Definieer de functie drawFigure
def drawFigure():
    return html.Div([
        dcc.Graph(
            figure={'data': [{'x': [1, 2, 3], 'y': [4, 4, 1], 'type': 'bar', 'name': 'SF'}],
                    'layout': {'title': 'Dash Data Visualization'}}
        )
    ])


# Definieer de lay-out van het dashboard
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row(
                html.H1('Lasermicrofoon', style={'fontsize': 40, 'textAlign': 'center'})
            ),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    dbc.DropdownMenu([
                        dbc.DropdownMenuItem('FIR'),
                        dbc.DropdownMenuItem('IIR'),
                        dbc.DropdownMenuItem('...'),
                    ])
                ])
            ]),
            html.Hr(),

            dbc.Row([
                dbc.Col([
                    drawFigure()
                ], width=6),
                dbc.Col([
                    drawFigure()
                ], width=6),
            ]),
        ]),
    ),
    html.Div([
        dbc.Button(id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            children=[
                dbc.Label("Voer gewenste frequentie in:"),
                dbc.Input(
                    id='frequency-input',
                    type='number',
                    value=get_latest_frequency(),
                    min=1,
                    max=20000,
                    step=1,
                    placeholder='Frequentie'
                ),

                dbc.ListGroup([
                    dbc.ListGroupItem("300Hz", id="300Hz", n_clicks=0, action=True),
                    dbc.ListGroupItem("400Hz", id="400Hz", n_clicks=0, action=True),
                    dbc.ListGroupItem("500Hz", id="500Hz", n_clicks=0, action=True),
                    dbc.ListGroupItem("600Hz", id="600Hz", n_clicks=0, action=True),
                    dbc.ListGroupItem("700Hz", id="700Hz", n_clicks=0, action=True),
                    dbc.ListGroupItem("800Hz", id="800Hz", n_clicks=0, action=True),
                ]),
            ],
            id="offcanvas",
            title="Geluiden",
            is_open=False,
        ),
    ])
])


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=False)
