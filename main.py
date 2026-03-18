import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Estoque de Agrotóxicos",
    page_icon="🌱",
    layout="wide"
)

st.title("📊 Estoque Consolidado")

uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # =========================
    # SIDEBAR ESTILO PAINEL
    # =========================
    st.sidebar.title("🌱 Filtros de Estoque")

    def filtro_selectbox(label, coluna):
        opcoes = ["TODOS"] + sorted(df[coluna].dropna().unique().tolist())
        escolha = st.sidebar.selectbox(label, opcoes)
        if escolha != "TODOS":
            return df[coluna] == escolha
        return pd.Series([True] * len(df))

    filtro = (
        filtro_selectbox("📍 Regional", "Departamento Regional") &
        filtro_selectbox("🏙️ Município", "Município") &
        filtro_selectbox("🏢 Empresa", "Empresa") &
        filtro_selectbox("📄 Nº Documento", "Nº Documento") &
        filtro_selectbox("📦 Tipo de Embalagem", "Descrição da Embalagem")
    )

    df_filtrado = df[filtro]

    st.sidebar.markdown("---")

    # =========================
    # BUSCAS
    # =========================
    st.sidebar.subheader("🔎 Busca por Produto")

    busca_produto = st.sidebar.text_input("Nome (Marca Comercial)")
    busca_lote = st.sidebar.text_input("Nº do Lote")

    if busca_produto:
        df_filtrado = df_filtrado[
            df_filtrado["Marca Comercial"].astype(str).str.contains(busca_produto, case=False, na=False)
        ]

    if busca_lote:
        df_filtrado = df_filtrado[
            df_filtrado["Nº do Lote"].astype(str).str.contains(busca_lote, case=False, na=False)
        ]

    # =========================
    # TOGGLE (APENAS COM SALDO)
    # =========================
    apenas_saldo = st.sidebar.toggle("Apenas com saldo", value=False)

    if apenas_saldo:
        df_filtrado = df_filtrado[df_filtrado["Saldo"] > 0]

    # =========================
    # MÉTRICAS
    # =========================
    st.subheader("📊 Indicadores")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total em Estoque", f"{df_filtrado['Saldo'].sum():,.2f}")
    col2.metric("Registros", len(df_filtrado))
    col3.metric("Empresas", df_filtrado["Empresa"].nunique())

    # =========================
    # TABELA
    # =========================
    st.subheader("📋 Resultado")

    st.dataframe(df_filtrado, use_container_width=True)

    # =========================
    # DOWNLOAD
    # =========================
    csv = df_filtrado.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Baixar CSV",
        csv,
        "estoque_filtrado.csv",
        "text/csv"
    )

else:
    st.info("Envie uma planilha para começar.")
