import hvplot.pandas
import pandas as pd
import streamlit as st
import plotly.express as px 
import matplotlib.pyplot as plt
from app.filter_data import getFilteredData
from app.load_data import loadData
from app.inputs_data import getListEmpresa, getListStatus, getListUfs, getMaxQtdPalavras, getMinMaxDate

df = loadData()

# dados para os inputs
empresas = getListEmpresa(df)
ufs = getListUfs(df)
status = getListStatus(df)
min_date, max_date = getMinMaxDate(df)
max_qtd_palavras = getMaxQtdPalavras(df)

# APP inicio
st.title('Reclame Aqui')

#crie um sidebar com os inputs
empresas_select = st.sidebar.selectbox('Selecione a empresa', empresas)
uf_select = st.sidebar.selectbox('Selecione o estado', ufs)
status_select = st.sidebar.selectbox('Selecione o status', status)

qtd_palavras_select = st.sidebar.slider(
    'Selecione a quantidade de palavras na descrição',
    min_value=0,
    max_value=max_qtd_palavras,
    value=(0, max_qtd_palavras))

data_select = st.sidebar.date_input(
    'Selecione a data', 
    min_value=min_date, 
    max_value=max_date, 
    value=(min_date, max_date))

# filtra os dados com base nos inputs
df_filtered = getFilteredData(df, empresas_select, uf_select, status_select, qtd_palavras_select, data_select)

total_reclamacoes=df_filtered['ID'].count()

st.metric(label="Total Reclamações", value=total_reclamacoes)


# cria um serie temporal do numero de reclamacoes por empresa por tempo
df_time = df_filtered.groupby(['empresa', 'TEMPO']).size().reset_index(name='reclamacoes')
fig = px.line(df_time, x='TEMPO', y='reclamacoes', color='empresa', title='Reclamações por empresa')
st.plotly_chart(fig)

# cria um grafico de barras do numero de reclamacoes por estado e status
df_uf = df_filtered.groupby(['UF', 'STATUS']).size().reset_index(name='reclamacoes')
fig = px.bar(df_uf, x='UF', y='reclamacoes', color='STATUS', title='Reclamações por estado e status')
st.plotly_chart(fig)


# cria um grafico com a distribuicao do numero de palavras na descricao das reclamacoes
fig = px.histogram(df_filtered, x='QTD_DESCRICAO_PALAVRAS', title='Distribuição do número de palavras na descrição')
st.plotly_chart(fig)


