import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meu App", layout="wide")

st.title("📊 Meu primeiro app Streamlit")

arquivo = st.file_uploader("Envie uma planilha Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
    st.dataframe(df)

    coluna = st.selectbox("Escolha uma coluna", df.columns)
    st.write(df[coluna].value_counts())
