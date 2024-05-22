#%%
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


#%%
df = pd.read_csv("dataset.csv")
df

# %%
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

df

# %%
df.info()
# %%
df["Chamadas Realizadas"] = df['Chamadas Realizadas'].astype('int64')
df["Dia"] = df['Dia'].astype('int64')
df["Mês"] = df['Mês'].astype('int64')

df["Valor Pago"] = df["Valor Pago"].str.lstrip('R$ ')
df['Valor Pago'] = df['Valor Pago'].astype('float64')

df
# %%
df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = '1'
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = '0'

df['Status de Pagamento'] = df['Status de Pagamento'].astype('int64')

df

# %%
df.info()
# %%
# Gerando o graficos
## Vendas por Equipe
# %%
df1 = df.groupby('Equipe')['Valor Pago'].sum().reset_index()

fig1 = go.Figure(go.Bar(
    x=df1['Valor Pago'],
    y=df1['Equipe'],
    orientation="h",
    textposition="auto",
    text=df1['Valor Pago'],
    insidetextfont=dict(family='Times', size=12),
    )
)

fig1.show()

# %%
# chamdas medias por dia

df2 = df.groupby("Dia")['Chamadas Realizadas'].mean().reset_index()

fig2 = go.Figure(
    go.Scatter(
        x=df2['Dia'],
        y=df2['Chamadas Realizadas'],
        mode='lines',
        fill='tozeroy',
        name='Chamadas por dia'
    )
)

fig2.show()

fig2.add_annotation(text='Media de chamadas por dia',
                    xref='paper',yref='paper',
                    font=dict(size=20, color='gray'),
                    align="center", bgcolor="rgba(0,0,0,0.8)",
                    x=0.05, y=0.85, showarrow=False)

fig2.add_annotation(text=f"Media: {round(df2["Chamadas Realizadas"].mean(),2)}",
                    xref='paper',yref='paper',
                    font=dict(size=20, color='gray'),
                    align='center', bgcolor="rgba(0,0,0,0.8)",
                    x=0.05, y=0.55, showarrow=False)

fig2.show()

# %%
# chamadas por mes
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


fig4.show()

# %%
# valores pagos meio de propaganda

df3 = df.groupby(["Meio de Propaganda","Mês"])["Valor Pago"].sum().reset_index()

fig3 = px.line(df3,y="Valor Pago",x="Mês",color="Meio de Propaganda")

fig3.show()

# %%
# propaganda e PieChart
df11 = df.groupby("Meio de Propaganda")["Valor Pago"].sum().reset_index()

fig11 = px.pie(df11,values="Valor Pago",names="Meio de Propaganda",hole=7)

# %%
# ganhos por mes + segregação por equipe
df5 = df.groupby(["Equipe","Mês"])["Valor Pago"].sum().reset_index()
df5_group = df.groupby("Mês")["Valor Pago"].sum().reset_index()

fig5 = px.line(df5,x="Mês",y="Valor Pago",color="Equipe")
fig5.add_trace(go.Scatter(x=df5_group['Mês'],y=df5_group['Valor Pago'],mode='lines+markers',fill='tozeroy',name='Total'))

fig5.show()

# %%
# Pagos e não pagos 

df6 = df.groupby("Status de Pagamento")["Chamadas Realizadas"].sum().reset_index()

fig6 = go.Figure()
fig6.add_trace(go.Pie(labels=["Não Pago","Pago"],values=df6["Chamadas Realizadas"],hole=.6))

fig6.show()

# %%
# Indicadores - melhor consultor

# Agrupamento e soma
df7 = df.groupby(["Consultor", "Equipe"])["Valor Pago"].sum()
df7.sort_values(ascending=False, inplace=True)
df7 = df7.reset_index()  # Corrigido para reatribuir o resultado

# Criação do gráfico
fig7 = go.Figure()

fig7.add_trace(go.Indicator(
    mode='number+delta',
    title={
        'text': f"<span style='font-size:150%'>{df7['Consultor'].iloc[0]} - Top Consultant</span><br>"
                f"<span style='font-size:70%'>Em vendas - em relação a média</span><br>"
    },
    value=df7['Valor Pago'].iloc[0],
    number={'prefix': "R$ "},
    delta={'relative': True, 'valueformat': '.1%', 'reference': df7['Valor Pago'].mean()}
)

fig7.show()
#%%
# Melhor Equipe
df8 = df.groupby("Equipe")["Valor Pago"].sum()
df8.sort_values(ascending=False, inplace=True)
df8 = df8.reset_index()  # Corrigido para reatribuir o resultado

# Criação do gráfico
fig8 = go.Figure()

fig8.add_trace(go.Indicator(
    mode='number+delta',
    title={
        'text': f"<span style='font-size:150%'>{df8['Equipe'].iloc[0]} - Top Equipe</span><br>"
                f"<span style='font-size:70%'>Em vendas - em relação a média</span><br>"
    },
    value=df8['Valor Pago'].iloc[0],
    number={'prefix': "R$ "},
    delta={'relative': True, 'valueformat': '.1%', 'reference': df8['Valor Pago'].mean()}
))

fig8.show()
#%% Ganhos totais
fig9 = go.Figure()
fig9.add_trace(go.Indicator(
    mode='number',
    title={
        'text': f"<span style='font-size:150%'>Valor Total</span>"},
        value= df['Valor Pago'].sum(),
        number={'prefix': "R$ "},
))
fig9.show()

#%% Total dos Chamados
fig10 = go.Figure()
fig10.add_trace(go.Indicator(
    mode='number',
    title={
        'text': f"<span style='font-size:150%'>Total de Chamados</span>"},
        value= len(df[df['Status de Pagamento'] == 1]),
))
fig10.show()
#%%
# top consultor por equipee seus valores de venda
df13 = df.groupby(["Consultor","Equipe"])["Valor Pago"].sum()
df13 = df13.sort_values(ascending=False)
df13 = df13.groupby("Equipe").head(1).reset_index()

fig13 = go.Figure(go.Pie(labels=df13["Consultor"] + ' - ' + df13["Equipe"], values=df13["Valor Pago"],hole=.6))

fig13.show()

#%%
# top consultor + equipe
fig14 = go.Figure(
    go.Bar(
        x=df13["Consultor"],
        y=df13["Valor Pago"],
        textposition="auto",
        text=df13["Valor Pago"],
        insidetextfont=dict(family='Times', size=12),
    )
)

fig14.show()
# %%
