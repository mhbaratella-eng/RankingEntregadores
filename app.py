import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Ranking de Entregadores",
    page_icon="🏆",
    layout="centered"
)

# ===============================
# CARREGAR DADOS
# ===============================

@st.cache_data
def carregar_dados():

    df = pd.read_csv(
        "ranking.csv",
        sep=";",
        encoding="cp1252",
        dtype=str
    )

    # Remove espaços dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Remove espaços dos dados
    for coluna in df.columns:
        if df[coluna].dtype == "object":
            df[coluna] = df[coluna].str.strip()

    # CPF apenas números
    df["cpf"] = df["cpf"].str.replace(r"\D", "", regex=True)

    # Rotas em número
    df["Rotas Completas"] = pd.to_numeric(
        df["Rotas Completas"],
        errors="coerce"
    ).fillna(0)

    # Ordena por rotas
    df = df.sort_values(
        by="Rotas Completas",
        ascending=False
    ).reset_index(drop=True)

    # Ranking Geral
    df["Posição Geral"] = range(1, len(df) + 1)

    # Ranking somente elegíveis
    elegiveis = df[
        df["Status"].str.contains(
            "elegível",
            case=False,
            na=False
        )
    ].copy()

    elegiveis["Posição Elegíveis"] = range(
        1,
        len(elegiveis) + 1
    )

    df = df.merge(
        elegiveis[["cpf", "Posição Elegíveis"]],
        on="cpf",
        how="left"
    )

    return df


df = carregar_dados()

# ===============================
# TÍTULO
# ===============================

st.title("🏆 Ranking de Entregadores")

st.write(
    "Digite seu CPF para consultar sua posição."
)

cpf = st.text_input(
    "CPF",
    placeholder="Digite somente os números"
)

# ===============================
# CONSULTA
# ===============================

if st.button("Consultar"):

    cpf = "".join(filter(str.isdigit, cpf))

    resultado = df[df["cpf"] == cpf]

    if resultado.empty:

        st.error("CPF não encontrado.")

    else:

        entregador = resultado.iloc[0]

        st.success("Consulta realizada com sucesso!")

        st.subheader(entregador["Entregador"])

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🏆 Ranking Geral",
                int(entregador["Posição Geral"])
            )

        with col2:

            if pd.notna(entregador["Posição Elegíveis"]):

                st.metric(
                    "✅ Ranking Elegíveis",
                    int(entregador["Posição Elegíveis"])
                )

            else:

                st.metric(
                    "✅ Ranking Elegíveis",
                    "-"
                )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🚴 Rotas",
                int(entregador["Rotas Completas"])
            )

        with col2:

            st.metric(
                "📈 Taxa de Aceite",
                entregador["% Taxa de Aceite"]
            )

        st.divider()

        status = entregador["Status"]

        if "elegível" in status.lower():

            st.success("🎉 Você está elegível para participar da campanha.")

        else:

            st.error("❌ Você ainda não está elegível.")

        st.subheader("Status")

        st.info(status)

        total = len(df)

        percentual = round(
            (1 - ((entregador["Posição Geral"] - 1) / total)) * 100
        )

        st.divider()

        st.write(
            f"Você está entre os **{percentual}%** melhores colocados do ranking geral."
        )

        st.progress(percentual / 100)
