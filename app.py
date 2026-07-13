# app.py

import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Ranking de Entregadores",
    page_icon="🏆",
    layout="centered"
)

try:
    st.image("logo.png", width=220)
except Exception:
    pass


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
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip()


    # Corrige CPF
    df["cpf"] = (
        df["cpf"]
        .str.replace(r"\D", "", regex=True)
        .str.zfill(11)
    )


    # Corrige rotas
    df["Rotas Completas"] = pd.to_numeric(
        df["Rotas Completas"],
        errors="coerce"
    ).fillna(0)


    # Ranking geral
    df = (
        df.sort_values(
            "Rotas Completas",
            ascending=False
        )
        .reset_index(drop=True)
    )

    df["Posição Geral"] = range(1, len(df) + 1)


    # Ranking elegíveis
    if "Status" in df.columns:

        eleg = df[
            df["Status"]
            .fillna("")
            .str.lower()
            .str.contains("eleg")
        ].copy()

        eleg["Posição Elegíveis"] = range(
            1,
            len(eleg) + 1
        )

        df = df.merge(
            eleg[["cpf", "Posição Elegíveis"]],
            on="cpf",
            how="left"
        )

    else:

        df["Posição Elegíveis"] = None


    return df



df = carregar_dados()


st.title("🏆 Ranking de Entregadores")


cpf = st.text_input(
    "CPF",
    placeholder="Digite somente os números"
)


if st.button("Consultar"):

    cpf = "".join(
        filter(str.isdigit, cpf)
    ).zfill(11)


    resultado = df[
        df["cpf"] == cpf
    ]


    if resultado.empty:

        st.error("CPF não encontrado.")


    else:

        e = resultado.iloc[0]


        st.success(
            "Consulta realizada com sucesso!"
        )


        st.subheader(
            e["Entregador"]
        )


        c1, c2 = st.columns(2)

with c1:
    pos = e["Posição Elegíveis"]

    st.metric(
        "🥇 Ranking Elegíveis",
        "-"
        if pd.isna(pos)
        else int(pos)
    )

with c2:
    st.metric(
        "🏆 Ranking Geral",
        int(e["Posição Geral"])
    )


        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "🏍️ Rotas",
                int(e["Rotas Completas"])
            )


        with c2:

            st.metric(
                "📈 Taxa de Aceite",
                e["% Taxa de Aceite"]
            )


        # Status / elegibilidade

        if "Status" in df.columns:

            status = str(e["Status"])

            obs = re.sub(
                r"^[^A-Za-zÀ-ÿ0-9?]+",
                "",
                status
            )

            obs = (
                obs
                .replace("??", "")
                .replace("?", "")
                .strip()
            )


            elegivel = (
                obs.lower()
                .startswith("eleg")
            )


            if elegivel:

                st.success(
                    "✅ Você está elegível."
                )

            else:

                st.error(
                    "❌ Você não está elegível."
                )


            st.subheader(
                "Observação"
            )

            st.info(obs)

        else:

            st.warning(
                "Coluna Status não encontrada no ranking."
            )
