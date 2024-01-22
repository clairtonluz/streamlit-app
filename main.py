import hvplot.pandas
import pandas as pd
import streamlit as st
import plotly.express as px 
import matplotlib.pyplot as plt

# Importa datasets
df_hapvida = pd.read_csv('datasets/RECLAMEAQUI_HAPVIDA.csv')
df_ibyte = pd.read_csv('datasets/RECLAMEAQUI_IBYTE.csv')
df_nagem = pd.read_csv('datasets/RECLAMEAQUI_NAGEM.csv')


df_hapvida['empresa'] = 'Hapvida'
df_ibyte['empresa'] = 'Ibyte'
df_nagem['empresa'] = 'Nagem'

df = pd.concat([df_hapvida, df_ibyte, df_nagem])
df['TEMPO'] = pd.to_datetime(df['TEMPO']).dt.date
df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')

# EMPRESAS
empresas = df['empresa'].dropna().unique()
empresas.sort()
empresas = ['TODAS'] + list(empresas)

# UF
ufs = df['UF'].dropna().unique()
ufs.sort()
ufs = ['TODOS'] + list(ufs)

# STATUS
status = df['STATUS'].dropna().unique()
status.sort()
status = ['TODOS'] + list(status)

# range de datas
min_date = df['TEMPO'].min()
max_date = df['TEMPO'].max()

# quantidade de palavras no campo 'DESCRICAO'
df['QTD_DESCRICAO_PALAVRAS'] = df['DESCRICAO'].apply(lambda x: len(x.split(' ')))
max_qtd_palavras = df['QTD_DESCRICAO_PALAVRAS'].max()


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

# crie um filtro para o dataframe usando os valores selecionados se for diferente de TODOS
df_filtered = df
if empresas_select != 'TODAS':
    df_filtered = df_filtered[df_filtered['empresa'] == empresas_select]
if uf_select != 'TODOS':
    df_filtered = df_filtered[df_filtered['UF'] == uf_select]
if status_select != 'TODOS':
    df_filtered = df_filtered[df_filtered['STATUS'] == status_select]
df_filtered = df_filtered[
    (df_filtered['QTD_DESCRICAO_PALAVRAS'] >= qtd_palavras_select[0]) &
    (df_filtered['QTD_DESCRICAO_PALAVRAS'] <= qtd_palavras_select[1])
]

# verificar se as datas selecionadas não são null
if len(data_select) == 2:
    df_filtered = df_filtered[
        (df_filtered['TEMPO'] >= data_select[0]) &
        (df_filtered['TEMPO'] <= data_select[1])
    ]

total_reclamacoes=df_filtered['QTD_DESCRICAO_PALAVRAS'].count()
col1, col2= st.columns(2)
col1.metric(label="Total Reclamações", value=total_reclamacoes)


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


