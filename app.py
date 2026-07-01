import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Ranking de Entregadores",
    page_icon="🏆",
    layout="centered"
)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("ranking.csv", dtype={"cpf": str})
    df["cpf"] = df["cpf"].str.replace(r"\D", "", regex=True)
    return df

df = carregar_dados()

st.title("🏆 Ranking de Entregadores")

cpf = st.text_input(
    "Digite seu CPF",
    placeholder="Somente números"
)

if st.button("Consultar"):

    cpf = "".join(filter(str.isdigit, cpf))

    resultado = df[df["cpf"] == cpf]

    if resultado.empty:
        st.error("CPF não encontrado.")
    else:
        linha = resultado.iloc[0]

        st.success("Entregador encontrado!")

        st.metric("Posição", f"{linha['Posicao']}º")

        st.write("**Nome:**", linha["Entregador"])

        total = len(df)

        porcentagem = round((1 - (linha["Posicao"]-1)/total)*100)

        st.progress(porcentagem/100)

        st.write(f"Você está entre os **{porcentagem}%** melhores colocados.")
