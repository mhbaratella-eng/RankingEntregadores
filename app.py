import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Ranking EntreGÔ Semanal",
    page_icon="🏆",
    layout="centered"
)

# Logo
st.image("logo.png", width=220)

# Título
st.title("🏆 Consulta de Ranking")

st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y')}")

st.divider()

# Escolha da filial
filial = st.radio(
    "Selecione sua cidade",
    ["São Paulo", "Goiânia", "Brasília"],
    horizontal=True
)

arquivos = {
    "São Paulo": "ranking-sp.xlsx",
    "Goiânia": "ranking-goiania.xlsx",
    "Brasília": "ranking-brasilia.xlsx"
}

try:
    df = pd.read_excel(arquivos[filial])

    df.columns = df.columns.str.strip().str.upper()

    df["CPF"] = (
        df["CPF"]
        .astype(str)
        .str.replace(r"\D", "", regex=True)
    )

except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
    st.stop()

st.divider()

cpf = st.text_input(
    "Digite seu CPF",
    placeholder="Somente números"
)

cpf = cpf.replace(".", "").replace("-", "").strip()

if st.button("Consultar", use_container_width=True):

    resultado = df[df["CPF"] == cpf]

    if resultado.empty():
        st.error("CPF não encontrado para esta filial.")

    else:
        nome = resultado.iloc[0]["NOME"]
        posicao = resultado.iloc[0]["POSIÇÃO"]

        st.success(f"Olá, **{nome}**!")

        st.metric(
            "🏆 Sua posição",
            f"{posicao}º"
        )

        st.balloons()
