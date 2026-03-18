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
    st.sidebar.subheader("🔎 Busca")

    busca_produto = st.sidebar.text_input("Marca Comercial")
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
    # APENAS COM SALDO
    # =========================
    apenas_saldo = st.sidebar.toggle("Apenas com saldo", value=True)

    if apenas_saldo:
        df_filtrado = df_filtrado[df_filtrado["Saldo"] > 0]

    # =========================
    # AGRUPAMENTO (PROFISSIONAL)
    # =========================
    df_filtrado = df_filtrado.groupby(
        ["Marca Comercial", "Nº do Lote", "Empresa", "Descrição da Embalagem"],
        as_index=False
    )["Saldo"].sum()

    # =========================
    # MÉTRICAS
    # =========================
    st.subheader("📊 Indicadores")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total em Estoque", f"{df_filtrado['Saldo'].sum():,.2f}")
    col2.metric("Produtos", df_filtrado["Marca Comercial"].nunique())
    col3.metric("Empresas", df_filtrado["Empresa"].nunique())

    # =========================
    # CARDS PROFISSIONAIS
    # =========================
    st.subheader("📦 Produtos")

    df_show = df_filtrado.sort_values(by="Saldo", ascending=False).head(50)

    html = """
    <style>
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 15px;
    }
    .card {
        background: #f9fafb;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .titulo {
        color: #2e7d32;
        font-weight: bold;
        font-size: 16px;
    }
    .lote {
        background: #d1fae5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        display: inline-block;
        margin-top: 5px;
    }
    .saldo {
        font-size: 18px;
        font-weight: bold;
    }
    </style>

    <div class="grid">
    """

    for _, row in df_show.iterrows():
        cor = "#2e7d32" if row["Saldo"] > 0 else "#c62828"

        html += f"""
        <div class="card" style="border-left:6px solid {cor};">
            <div class="titulo">{row['Marca Comercial']}</div>
            
            <div>📦 {row['Descrição da Embalagem']}</div>
            
            <div class="lote">Lote: {row['Nº do Lote']}</div>

            <div style="margin-top:10px;">🏢 {row['Empresa']}</div>

            <hr>

            <div style="display:flex; justify-content:space-between;">
                <span>SALDO</span>
                <span class="saldo" style="color:{cor};">
                    {row['Saldo']}
                </span>
            </div>
        </div>
        """

    html += "</div>"

    components.html(html, height=900, scrolling=True)

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
