# app.py

import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Ranking Meta do foguete",
    page_icon="🚀",
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

    df.columns = df.columns.str.strip()

    for c in df.columns:
        df[c] = df[c].astype(str).str.strip()


    # Ajuste CPF
    df["cpf"] = (
        df["cpf"]
        .str.replace(r"\D", "", regex=True)
        .str.zfill(11)
    )


    # Ajuste de rotas
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


    df["Posição Geral"] = range(
        1,
        len(df) + 1
    )


    # Ranking elegíveis limitado aos 40 primeiros

    if "Status" in df.columns:


        eleg = df[
            df["Status"]
            .fillna("")
            .str.lower()
            .str.contains("eleg")
        ].copy()


        # Apenas os 40 primeiros elegíveis entram
        eleg = eleg.head(40)


        eleg["Posição Elegíveis"] = range(
            1,
            len(eleg) + 1
        )


        df = df.merge(
            eleg[["cpf", "Posição Elegíveis"]],
            on="cpf",
            how="left"
        )


        # Quem era elegível mas ficou fora dos 40
        # passa a ser inelegível

        df.loc[
            (
                df["Status"]
                .fillna("")
                .str.lower()
                .str.contains("eleg")
            )
            &
            (
                df["Posição Elegíveis"].isna()
            ),
            "Status"
        ] = "Inelegível"


    else:

        df["Posição Elegíveis"] = None


    return df



df = carregar_dados()


st.title("🚀 Ranking Meta do foguete")


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


        st.error(
            "CPF não encontrado."
        )


    else:


        e = resultado.iloc[0]


        st.success(
            "Consulta realizada com sucesso!"
        )


        st.subheader(
            e["Entregador"]
        )



        # Rankings

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



        # Dados de performance

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



        # Status

        if "Status" in df.columns:


            status = str(
                e["Status"]
            )


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
                not pd.isna(e["Posição Elegíveis"])
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


            st.info(
                obs
            )


        else:


            st.warning(
                "Coluna Status não encontrada no ranking."
            )
            # Banner da promoção
try:
    st.image("banner.jpg", use_container_width=True)
except Exception:
    pass
