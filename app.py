import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Ranking EntreGÔ Semanal",
    page_icon="🏆"
)

st.title("🏆 Ranking da OL")

try:
    df = pd.read_excel("ranking.xlsx")

    df["CPF"] = df["CPF"].astype(str)

except Exception as e:
    st.error(e)

cpf = st.text_input(
    "Digite seu CPF",
    type="password"
)

if st.button("Consultar"):

    resultado = df[df["CPF"] == cpf]

    if resultado.empty:
        st.error("CPF não encontrado.")

    else:
        nome = resultado.iloc[0]["Nome"]
        posicao = resultado.iloc[0]["Posição"]

        st.success(f"Olá, {nome}!")

        st.metric(
            label="Sua posição no ranking",
            value=f"{posicao}º"
        )
