from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
import dash

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME])
app.scripts.config.serve_locally = True
server = app.server

# ======== STYLES ===========
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor": "top", "y": 0.9, "xanchor": "left", "x": 0.1, "title": {"text": None}, "font": {"color": "white"}, "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l": 10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# ======== LEITURA CSV ==========
df = pd.read_csv("dataset.csv")
df_cru = df.copy()

# ======== MESES EM NUMEROS ========
meses = {'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04', 'Mai': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12'}
df['Mês'] = df['Mês'].map(meses)

# ======== LIMPEZA DE DADOS ========
df["Chamadas Realizadas"] = df['Chamadas Realizadas'].astype('int64')
df["Dia"] = df['Dia'].astype('int64')
df["Mês"] = df['Mês'].astype('int64')
df["Valor Pago"] = df["Valor Pago"].str.lstrip('R$ ').astype('float64')
df['Status de Pagamento'] = df['Status de Pagamento'].map({'Pago': 1, 'Não pago': 0}).astype('int64')

# Criando opções para os filtros
options_month = [{'label': 'Ano todo', 'value': 0}] + [{'label': i, 'value': j} for i, j in zip(df_cru["Mês"].unique(), df["Mês"].unique())]
options_month = sorted(options_month, key=lambda x: x['value'])

options_team = [{'label': 'Toda Equipe', 'value': 0}] + [{'label': i, 'value': i} for i in df["Equipe"].unique()]

# Função dos filtros
def month_filter(month):
    if month == 0:
        return df['Mês'].isin(df["Mês"].unique())
    else:
        return df['Mês'] == month
    
def team_filter(team):
    if team == 0:
        return df['Equipe'].isin(df["Equipe"].unique())
    else:
        return df['Equipe'] == team

def convert_to_text(month):
    lista1 = ['Ano todo', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    return lista1[month]

# ======== LAYOUT ===========
app.layout = dbc.Container(children=[
    # Linha 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([html.Legend("Sales Analytics")], sm=8),
                        dbc.Col([html.I(className='fa fa-balance-scale', style={'font-size': '300%'})], sm=4, align="center")
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
                    dbc.Row(dbc.Col(html.Legend('Top Consultores por Equipe'))),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='graph1', className='dbc', config=config_graph)], sm=12, md=7),
                        dbc.Col([dcc.Graph(id='graph2', className='dbc', config=config_graph)], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(dbc.Col([
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
                    ]))
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    
    # Linha 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([dcc.Graph(id='graph3', className='dbc', config=config_graph)])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([dcc.Graph(id='graph4', className='dbc', config=config_graph)])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([dcc.Graph(id='graph5', className='dbc', config=config_graph)])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([dcc.Graph(id='graph6', className='dbc', config=config_graph)])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([dcc.Graph(id='graph7', className='dbc', config=config_graph)], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([dcc.Graph(id='graph8', className='dbc', config=config_graph)], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Linha 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Distribuição de Propaganda'),
                    dcc.Graph(id='graph9', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Valores de Propaganda convertidos por mês"),
                    dcc.Graph(id='graph10', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(id='graph11', className='dbc', config=config_graph)])
            ], style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha a Equipe'),
                    dbc.RadioItems(
                        id="radio-team",
                        options=options_team,
                        value=0,
                        inline=True,
                        labelCheckedClassName="text-warning",
                        inputCheckedClassName="border border-warning bg-warning",
                    ),
                    html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '100vh'})

# ======== CALLBACKS ========
# callback para linha 1
@app.callback(
    [Output('graph1', 'figure'), 
     Output('graph2', 'figure'), 
     Output('month-select', 'children')],
    [Input('radio-month', 'value'), 
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def update_graphs(month, toggle):
    template = template_theme1 if toggle else template_theme2
    mask = month_filter(month)
    df_filtered = df[mask]

    df_grouped = df_filtered.groupby(['Equipe', 'Consultor'])['Valor Pago'].sum().sort_values(ascending=False).reset_index()
    top_consultants = df_grouped.groupby('Equipe').head(1)

    fig1 = go.Figure(go.Bar(x=top_consultants['Valor Pago'], y=top_consultants['Equipe'], 
                            textposition="auto", text=top_consultants['Valor Pago'], orientation='h'))
    fig2 = go.Figure(go.Pie(labels=top_consultants['Consultor'] + ' - ' + top_consultants['Equipe'],
                             values=top_consultants['Valor Pago'], hole=.6))

    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template, showlegend=False)

    select = html.H1(convert_to_text(month))

    return fig1, fig2, select

# callback para linha 2
@app.callback(
    Output('graph3', 'figure'), 
    [Input('radio-team', 'value'), 
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def graph3(team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = team_filter(team)
    df_filtered = df[mask]
    df2 = df.groupby("Dia")['Chamadas Realizadas'].mean().reset_index()

    fig3 = go.Figure(
        go.Scatter(
            x=df2['Dia'],
            y=df2['Chamadas Realizadas'],
            mode='lines',
            fill='tozeroy',
            name='Chamadas por dia'
        )
    )

    fig3.add_annotation(text='Media de chamadas por dia',
                        xref='paper',yref='paper',
                        font=dict(size=20, color='gray'),
                        align="center", bgcolor="rgba(0,0,0,0.8)",
                        x=0.05, y=0.85, showarrow=False)

    fig3.add_annotation(text=f"Media: {round(df2["Chamadas Realizadas"].mean(),2)}",
                        xref='paper',yref='paper',
                        font=dict(size=20, color='gray'),
                        align='center', bgcolor="rgba(0,0,0,0.8)",
                        x=0.05, y=0.55, showarrow=False)

    fig3.update_layout(main_config, height=180, template=template)


    return fig3

@app.callback(
    Output('graph4', 'figure'), 
    [Input('radio-team', 'value'), 
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def graph4(team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = team_filter(team)
    df4 = df.groupby("Mês")["Chamadas Realizadas"].sum().reset_index()

    fig4 = go.Figure(
            go.Scatter(x=df4['Mês'],y=df4['Chamadas Realizadas'],mode='lines',fill='tozeroy',name='Chamadas por mes')
    )

    fig4.add_annotation(text='Media de chamadas por Mês',
                        xref='paper',yref='paper',
                        font=dict(size=20, color='gray'),
                        align="center", bgcolor="rgba(0,0,0,0.8)",
                        x=0.05, y=0.85, showarrow=False)

    fig4.add_annotation(text=f"Media: {round(df4["Chamadas Realizadas"].mean(),2)}",
                        xref='paper',yref='paper',
                        font=dict(size=20, color='gray'),
                        align='center', bgcolor="rgba(0,0,0,0.8)",
                        x=0.05, y=0.55, showarrow=False)

    fig4.update_layout(main_config, height=180, template=template)

    return fig4

# indicadores 5 e 6 graph 5 e 6
@app.callback(
    [Output('graph5', 'figure'),
     Output('graph6', 'figure')],  
    [Input('radio-team', 'value'), 
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def graph5(team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = team_filter(team)
    df5 = dg6 = df.loc[mask]

    df5 = df.groupby(["Consultor", "Equipe"])["Valor Pago"].sum()
    df5.sort_values(ascending=False, inplace=True)
    df5 = df5.reset_index()  # Corrigido para reatribuir o resultado

    # Criação do gráfico
    fig5 = go.Figure()

    fig5.add_trace(go.Indicator(
        mode='number+delta',
        title={
            'text': f"<span style='font-size:70%'>{df5['Consultor'].iloc[0]} - Top Consultant</span><br>"
                    f"<span style='font-size:50%'>Em vendas - em relação a média</span><br>"
        },
        value=df5['Valor Pago'].iloc[0],
        number={'prefix': "R$ "},
        delta={'relative': True, 'valueformat': '.1%', 'reference': df5['Valor Pago'].mean()}
    ))
    # Melhor Equipe
    df6 = df.groupby("Equipe")["Valor Pago"].sum()
    df6.sort_values(ascending=False, inplace=True)
    df6 = df6.reset_index()  # Corrigido para reatribuir o resultado

    # Criação do gráfico
    fig6 = go.Figure()

    fig6.add_trace(go.Indicator(
        mode='number+delta',
        title={
            'text': f"<span style='font-size:70%'>{df6['Equipe'].iloc[0]} - Top Equipe</span><br>"
                    f"<span style='font-size:50%'>Em vendas - em relação a média</span><br>"
        },
        value=df6['Valor Pago'].iloc[0],
        number={'prefix': "R$ "},
        delta={'relative': True, 'valueformat': '.1%', 'reference': df6['Valor Pago'].mean()}
    ))

    fig5.update_layout(main_config, height=200, template=template)
    fig6.update_layout(main_config, height=200, template=template)
    fig5.update_layout({"margin": {"t": 0, "b": 0, "l": 50, "r": 0}})
    fig6.update_layout({"margin": {"t": 0, "b": 0, "l": 50, "r": 0}})


    return fig5, fig6

# graph 7
@app.callback(
    Output('graph7', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(toggle):
    template = template_theme1 if toggle else template_theme2

    df_7 = df.groupby(['Mês', 'Equipe'])['Valor Pago'].sum().reset_index()
    df_7_group = df.groupby('Mês')['Valor Pago'].sum().reset_index()
    
    fig7 = px.line(df_7, y="Valor Pago", x="Mês", color="Equipe")
    fig7.add_trace(go.Scatter(y=df_7_group["Valor Pago"], x=df_7_group["Mês"], mode='lines+markers', fill='tonexty', name='Total de Vendas'))

    fig7.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=190, template=template)
    fig7.update_layout({"legend": {"yanchor": "top", "y":0.99, "font" : {"color":"white", 'size': 10}}})
    return fig7

# graph 8
@app.callback(
    Output('graph8', 'figure'),  
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph8(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df8 = df.loc[mask]


    df8 = df.groupby('Equipe')['Valor Pago'].sum().reset_index()

    fig8 = go.Figure(go.Bar(
    x=df8['Valor Pago'],
    y=df8['Equipe'],
    orientation="h",
    textposition="auto",
    text=df8['Valor Pago'],
    insidetextfont=dict(family='Times', size=12),
    )
)

    fig8.update_layout(main_config, height=360, template=template)

    return fig8

@app.callback(
    Output('graph9', 'figure'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph9(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df9 = df.loc[mask]

    mask = team_filter(team)
    df9 = df9.loc[mask]

    df9_group = df.groupby("Mês")["Valor Pago"].sum().reset_index()

    fig9 = go.Figure()
    fig9.add_trace(go.Pie(labels=df9['Meio de Propaganda'], values=df9['Valor Pago'], hole=.7))

    fig9.update_layout(main_config, height=150, template=template, showlegend=False)
    return fig9

@app.callback(
    Output('graph10', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph10(team, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = team_filter(team)
    df10 = df.loc[mask]

    df10 = df10.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
    fig10 = px.line(df10, y="Valor Pago", x="Mês", color="Meio de Propaganda")

    fig10.update_layout(main_config, height=200, template=template, showlegend=False)
    return fig10

@app.callback(
    Output('graph11', 'figure'),
    Output('team-select', 'children'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph11(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_11 = df.loc[mask]

    mask = team_filter(team)
    df_11 = df_11.loc[mask]

    fig11 = go.Figure()
    fig11.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Valor Total</span><br><span style='font-size:70%'>Em Reais</span><br>"},
        value = df_11['Valor Pago'].sum(),
        number = {'prefix': "R$"}
    ))

    fig11.update_layout(main_config, height=300, template=template)
    select = html.H1("Todas Equipes") if team == 0 else html.H1(team)

    return fig11, select

# callback para linha 3

# ======== RUN APP ==========
if __name__ == "__main__":
    app.run_server(debug=True)
