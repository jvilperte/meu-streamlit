import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Estoque de Agrotóxicos",
    page_icon="🌱",
    layout="wide"
)

st.title("📊 Estoque Consolidado")

# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader("📁 Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # =========================
    # SIDEBAR (FILTROS)
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
    # BUSCA
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
    # TOGGLE
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
    # CARDS (HTML via COMPONENTS)
    # =========================
    st.subheader("📦 Produtos")

    df_show = df_filtrado.head(50)

    html_cards = """
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;">
    """

    for _, row in df_show.iterrows():
        html_cards += f"""
        <div style="
            background-color:#f9fafb;
            padding:20px;
            border-radius:12px;
            border-left:6px solid #2e7d32;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
        ">
            <h4 style="margin:0;color:#2e7d32;">{row['Marca Comercial']}</h4>

            <p style="margin:5px 0;">📦 {row['Descrição da Embalagem']}</p>

            <span style="
                background:#d1fae5;
                color:#065f46;
                padding:4px 10px;
                border-radius:8px;
                font-size:12px;">
                Lote: {row['Nº do Lote']}
            </span>

            <p style="margin-top:10px;">🏢 {row['Empresa']}</p>

            <hr>

            <div style="display:flex; justify-content:space-between;">
                <span><b>SALDO DISPONÍVEL</b></span>
                <span style="color:#1d4ed8; font-size:18px;">
                    <b>{row['Saldo']}</b>
                </span>
            </div>
        </div>
        """

    html_cards += "</div>"

    components.html(html_cards, height=800, scrolling=True)

    # =========================
    # DOWNLOAD
    # =========================
    st.subheader("⬇️ Exportar")

    csv = df_filtrado.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Baixar dados filtrados (CSV)",
        csv,
        "estoque_filtrado.csv",
        "text/csv"
    )

else:
    st.info("👆 Faça upload da planilha para começar.")
