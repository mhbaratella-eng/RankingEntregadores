# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ranking de Entregadores", page_icon="🏆", layout="centered")

try:
    st.image("logo.png", width=220)
except Exception:
    pass

@st.cache_data
def carregar_dados():
    df = pd.read_csv("ranking.csv", sep=";", encoding="cp1252", dtype=str)
    df.columns = df.columns.str.strip()

    for c in df.columns:
        df[c] = df[c].astype(str).str.strip()

    df["cpf"] = (
        df["cpf"]
        .str.replace(r"\D", "", regex=True)
        .str.zfill(11)
    )

    df["Rotas Completas"] = pd.to_numeric(df["Rotas Completas"], errors="coerce").fillna(0)

    df = df.sort_values("Rotas Completas", ascending=False).reset_index(drop=True)
    df["Posição Geral"] = range(1, len(df)+1)

    eleg = df[df["Status"].fillna("").str.lower().str.contains("eleg")].copy()
    eleg["Posição Elegíveis"] = range(1, len(eleg)+1)

    df = df.merge(eleg[["cpf","Posição Elegíveis"]], on="cpf", how="left")
    return df

df = carregar_dados()

st.title("🏆 Ranking de Entregadores")
cpf = st.text_input("CPF", placeholder="Digite somente os números")

if st.button("Consultar"):
    cpf = "".join(filter(str.isdigit, cpf)).zfill(11)
    resultado = df[df["cpf"] == cpf]

    if resultado.empty:
        st.error("CPF não encontrado.")
    else:
        e = resultado.iloc[0]
        st.success("Consulta realizada com sucesso!")
        st.subheader(e["Entregador"])
        c1,c2 = st.columns(2)
        with c1:
            st.metric("🏆 Ranking Geral", int(e["Posição Geral"]))
        with c2:
            pos = e["Posição Elegíveis"]
            st.metric("🥇 Ranking Elegíveis", "-" if pd.isna(pos) else int(pos))
        c1,c2 = st.columns(2)
        with c1:
            st.metric("🏍️ Rotas", int(e["Rotas Completas"]))
        with c2:
            st.metric("📈 Taxa de Aceite", e["% Taxa de Aceite"])

        status = str(entregador["Status"])

# Remove os "??" e espaços extras
status_limpo = (
    status
    .replace("??", "")
    .replace("?", "")
    .strip()
)
        if "eleg" in status.lower():

    st.success("✅ Você está elegível para participar da campanha.")

else:

    st.error("❌ Você não está elegível.")

st.subheader("Observação")
st.info(status_limpo)
