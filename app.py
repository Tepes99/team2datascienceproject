import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html


app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
        }
    ],
)
server = app.server

app.layout = html.Div([dash.page_container])

if __name__ == "__main__":
    app.run_server(debug=True)
