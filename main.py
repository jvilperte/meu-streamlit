import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Estoque de Agrotóxicos",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Controle de Estoque de Agrotóxicos")

# Upload do arquivo
uploaded_file = st.file_uploader("📁 Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.success("Arquivo carregado com sucesso!")

    # ====== LIMPEZA BÁSICA ======
    df.columns = df.columns.str.strip()

    # ====== SIDEBAR FILTROS ======
    st.sidebar.header("🔎 Filtros")

    # Município
    municipios = st.sidebar.multiselect(
        "Município",
        options=sorted(df["Município"].dropna().unique())
    )

    # Nº Documento
    documentos = st.sidebar.multiselect(
        "Nº Documento",
        options=sorted(df["Nº Documento"].dropna().unique())
    )

    # Empresa
    empresas = st.sidebar.multiselect(
        "Empresa",
        options=sorted(df["Empresa"].dropna().unique())
    )

    # Descrição da Embalagem
    embalagens = st.sidebar.multiselect(
        "Descrição da Embalagem",
        options=sorted(df["Descrição da Embalagem"].dropna().unique())
    )

    # ====== APLICAR FILTROS ======
    df_filtrado = df.copy()

    if municipios:
        df_filtrado = df_filtrado[df_filtrado["Município"].isin(municipios)]

    if documentos:
        df_filtrado = df_filtrado[df_filtrado["Nº Documento"].isin(documentos)]

    if empresas:
        df_filtrado = df_filtrado[df_filtrado["Empresa"].isin(empresas)]

    if embalagens:
        df_filtrado = df_filtrado[df_filtrado["Descrição da Embalagem"].isin(embalagens)]

    # ====== CAMPO DE PESQUISA ======
    st.subheader("🔍 Pesquisa")

    busca = st.text_input(
        "Digite Marca Comercial ou Nº do Lote:",
        placeholder="Ex: Roundup ou LOTE123"
    )

    if busca:
        busca = busca.lower()

        df_filtrado = df_filtrado[
            df_filtrado["Marca Comercial"].astype(str).str.lower().str.contains(busca) |
            df_filtrado["Nº do Lote"].astype(str).str.lower().str.contains(busca)
        ]

    # ====== MÉTRICAS ======
    st.subheader("📊 Indicadores")

    col1, col2, col3 = st.columns(3)

    total_saldo = df_filtrado["Saldo"].sum()
    col1.metric("Total em Estoque", f"{total_saldo:,.2f}")

    col2.metric("Registros Filtrados", len(df_filtrado))
    col3.metric("Empresas", df_filtrado["Empresa"].nunique())

    # ====== TABELA ======
    st.subheader("📋 Resultado")

    st.dataframe(df_filtrado, use_container_width=True)

    # ====== DOWNLOAD ======
    st.subheader("⬇️ Exportar")

    csv = df_filtrado.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Baixar dados filtrados (CSV)",
        data=csv,
        file_name="estoque_filtrado.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Faça upload da planilha para iniciar.")
