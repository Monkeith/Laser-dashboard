import dash
import dash_bootstrap_components as dbc
import dash_html_components as html 



app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    dbc.Alert("Hello Bootstrap!", color="success"),
    className="p-5",
)

if __name__ == "__main__":
    app.run_server()