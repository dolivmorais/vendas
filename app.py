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
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor": "top",
               "y": 0.9,
               "xanchor": "left",
                "x": 0.1,
                "title": {"text": None},
                "font":  {"color": "white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

#======== leitura csv ==========
df = pd.read_csv("dataset.csv")
df_cru = df.copy()

# ====== meses em numeros
df.loc[df['Mês'] == 'Jan', 'Mês'] = '01'
df.loc[df['Mês'] == 'Fev', 'Mês'] = '02'
df.loc[df['Mês'] == 'Mar', 'Mês'] = '03'
df.loc[df['Mês'] == 'Abr', 'Mês'] = '04'
df.loc[df['Mês'] == 'Mai', 'Mês'] = '05'
df.loc[df['Mês'] == 'Jun', 'Mês'] = '06'
df.loc[df['Mês'] == 'Jul', 'Mês'] = '07'
df.loc[df['Mês'] == 'Ago', 'Mês'] = '08'
df.loc[df['Mês'] == 'Set', 'Mês'] = '09'
df.loc[df['Mês'] == 'Out', 'Mês'] = '10'
df.loc[df['Mês'] == 'Nov', 'Mês'] = '11'
df.loc[df['Mês'] == 'Dez', 'Mês'] = '12'

#======== limpeza de dados ==========
df["Chamadas Realizadas"] = df['Chamadas Realizadas'].astype('int64')
df["Dia"] = df['Dia'].astype('int64')
df["Mês"] = df['Mês'].astype('int64')
df["Valor Pago"] = df["Valor Pago"].str.lstrip('R$ ')
df['Valor Pago'] = df['Valor Pago'].astype('float64')
df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = '1'
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = '0'
df['Status de Pagamento'] = df['Status de Pagamento'].astype('int64')


#criando opções pros filtros
options_month = [{'label': 'Ano todo', 'Value': 0}]
for i, j in zip(df_cru["Mês"].unique(), df["Mês"].unique()):
    options_month.append({'label': i, 'Value': j})
options_month = sorted(options_month, key=lambda x: x['Value'])

options_team = [{'label': 'Toda Equipe', 'Value': 0}]
for i in df["Equipe"].unique():
    options_team.append({'label': i, 'Value': i})


#======== layout ===========
app.layout = dbc.Container(children=[
    # linhha 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([  
                            html.Legend("Sales Analytics")
                        ], sm=8),
                        dbc.Col([        
                            html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Diego Morais")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite perfil no Linkedin", href="https://www.linkedin.com/in/oliveiradm/", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Top Consultores por Equipe')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'})
    ], fluid=True, style={'height': '100vh'})


#======== callbacks ========


#======== run app ==========


if __name__ == "__main__":
    app.run_server(debug=True)
