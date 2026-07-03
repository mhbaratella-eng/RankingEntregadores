import streamlit as st
import pandas as pd

# ==========================
# Configuração da página
# ==========================
st.set_page_config(
    page_title="Ranking EntreGÔ Semanal",
    page_icon="🏆",
    layout="centered"
)

# ==========================
# Cabeçalho
# ==========================

try:
    st.image("logo.png", width=220)
except:
    pass

st.title("🏆 Consulta de Ranking Semanal")
st.write("Consulte sua posição no ranking da sua cidade.")

st.divider()

# ==========================
# Escolha da filial
# ==========================

filial = st.radio(
    "Escolha sua cidade",
    ["São Paulo", "Goiânia", "Brasília"],
    horizontal=True
)

arquivos = {
    "São Paulo": "ranking-sp.xlsx",
    "Goiânia": "ranking-goiania.xlsx",
    "Brasília": "ranking-brasilia.xlsx"
}

# ==========================
# Carrega a planilha
# ==========================

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

# ==========================
# Consulta
# ==========================

cpf = st.text_input(
    "CPF",
    placeholder="Digite apenas os números"
)

cpf = cpf.replace(".", "").replace("-", "").strip()

st.write("")

if st.button("🔍 Consultar posição", use_container_width=True):

    resultado = df[df["CPF"] == cpf]

    if resultado.empty:
        st.error("CPF não encontrado nesta filial.")

    else:

        nome = resultado.iloc[0]["NOME"]
        posicao = resultado.iloc[0]["POSIÇÃO"]

        st.success(f"Bem-vindo(a), **{nome}**!")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🏆 Colocação",
                f"{posicao}º"
            )

        with col2:
            st.metric(
                "📍 Filial",
                filial
            )

        st.divider()

        if posicao == 1:
            st.info("🥇 Parabéns! Você é o líder do ranking!")

        elif posicao <= 10:
            st.info("🔥 Você está entre os 10 primeiros!")

        elif posicao <= 20:
            st.info("👏 Continue assim! Você está no Top 20!")

        st.balloons()
