import pandas as pd
import streamlit as st

def _formatData(df):
    df['TEMPO'] = pd.to_datetime(df['TEMPO']).dt.date
    df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')
    return df

@st.cache_data
def loadData():
    # Importa datasets
    df_hapvida = pd.read_csv('https://raw.githubusercontent.com/clairtonluz/streamlit-app/main/datasets/RECLAMEAQUI_HAPVIDA.csv')
    df_ibyte = pd.read_csv('https://raw.githubusercontent.com/clairtonluz/streamlit-app/main/datasets/RECLAMEAQUI_IBYTE.csv')
    df_nagem = pd.read_csv('https://raw.githubusercontent.com/clairtonluz/streamlit-app/main/datasets/RECLAMEAQUI_NAGEM.csv')
    df_hapvida['empresa'] = 'Hapvida'
    df_ibyte['empresa'] = 'Ibyte'
    df_nagem['empresa'] = 'Nagem'

    df = pd.concat([df_hapvida, df_ibyte, df_nagem])
    _formatData(df)
    return df
