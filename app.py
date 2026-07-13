import streamlit as st
import pandas as pd

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================

st.set_page_config(
    page_title="Ranking de Entregadores",
    page_icon="🏆",
    layout="centered"
)

# ============================================
# CARREGA O CSV
# ============================================

@st.cache_data
def carregar_dados():

    try:
        df = pd.read_csv(
            "ranking.csv",
            sep=";",
            encoding="utf-8-sig",
            dtype=str
        )
    except:
        df = pd.read_csv(
            "ranking.csv",
            encoding="utf-8-sig",
            dtype=str
        )

    # Remove espaços dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Remove espaços dos dados
    df = df.apply(lambda coluna: coluna.str.strip() if coluna.dtype == "object" else coluna)

    # CPF apenas números
    df["cpf"] = df["cpf"].str.replace(r"\D", "", regex=True)

    # Converte rotas para número
    df["Rotas Completas"] = (
        df["Rotas Completas"]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # Ordena pelo maior número de rotas
    df = df.sort_values(
        by="Rotas Completas",
        ascending=False
    ).reset_index(drop=True)

    # Cria posição geral
    df["Posição Geral"] = df.index + 1

    # Apenas elegíveis
    elegiveis = (
        df[
            df["Status"].str.lower() == "elegível".lower()
        ]
        .copy()
        .reset_index(drop=True)
    )

    # Cria posição dos elegíveis
    elegiveis["Posição Elegíveis"] = elegiveis.index + 1

    # Junta novamente
    df = df.merge(
        elegiveis[["cpf", "Posição Elegíveis"]],
        on="cpf",
        how="left"
    )

    return df

df = carregar_dados()

# ============================================
# CABEÇALHO
# ============================================

st.title("🏆 Ranking de Entregadores")

st.write("Digite seu CPF para consultar sua posição no ranking.")

cpf = st.text_input(
    "CPF",
    placeholder="Digite apenas os números"
)

# ============================================
# CONSULTA
# ============================================

if st.button("Consultar"):

    cpf = "".join(filter(str.isdigit, cpf))

    resultado = df[df["cpf"] == cpf]

    if resultado.empty:

        st.error("CPF não encontrado.")

    else:

        entregador = resultado.iloc[0]

        st.success("Consulta realizada com sucesso!")

        st.markdown(f"## {entregador['Entregador']}")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🏆 Posição Geral",
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

        if status.lower() == "elegível":

            st.success("🎉 Você está elegível para a campanha!")

        else:

            st.error("❌ Você ainda não está elegível.")

        st.subheader("Observação")

        st.info(entregador["Observação"])

        st.divider()

        total = len(df)

        percentual = round(
            (1 - ((entregador["Posição Geral"] - 1) / total)) * 100
        )

        st.write(
            f"Você está entre os **{percentual}%** primeiros colocados do ranking geral."
        )

        st.progress(percentual / 100)
