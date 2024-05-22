from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
import dash



FONT_AWESOOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOOME)
app.scripts.config.serve_locally = True
server = app.server


#======== sTYLES ===========


#======== layout ===========
app.layout = dbc.Container(children=[

    ], fluid=True, style={'height': '100vh'})



#======== callbacks ========


#======== run app ==========


if __name__ == "__main__":
    app.run_server(debug=True)
