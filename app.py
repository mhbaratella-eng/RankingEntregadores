import streamlit as st
import pandas as pd

# 1. Configuração da página
st.set_page_config(page_title="Ranking de Entregadores", page_icon="🛵", layout="centered")

# 2. Função para carregar os dados exatamente como estão na planilha
@st.cache_data
def carregar_dados():
    # Carrega a planilha tratando o CPF como texto para não sumir com zeros à esquerda
    df = pd.read_csv("ranking.csv", dtype={'cpf': str})
    return df

try:
    df_ranking = carregar_dados()
except FileNotFoundError:
    st.error("Erro: O arquivo 'ranking.csv' não foi encontrado no GitHub.")
    st.stop()

# 3. Interface Visual
st.title("🛵 Consulta de Ranking - Entregadores")
st.write("Insira seu CPF abaixo para verificar sua colocação atual.")

# Campo para o entregador digitar
cpf_digitado = st.text_input("Digite seu CPF (apenas números):", max_chars=14)

# 4. Lógica de Busca Oculta
if cpf_digitado:
    # Limpa pontos e traços que o entregador possa ter digitado
    cpf_limpo = cpf_digitado.strip().replace(".", "").replace("-", "")
    
    # Limpa a coluna de CPF da planilha para garantir que a comparação funcione perfeitamente
    df_ranking['cpf_limpo'] = df_ranking['cpf'].astype(str).str.replace(".", "", regex=False).str.replace("-", "", regex=False).str.strip()
    
    # Busca o entregador na tabela pelo CPF
    resultado = df_ranking[df_ranking['cpf_limpo'] == cpf_limpo]
    
    if not resultado.empty:
        # Puxa as informações das colunas exatas da sua planilha
        nome = resultado.iloc[0]['Entregador']
        posicao = resultado.iloc[0]['Posição']
        
        st.success(f"Olá, **{nome}**! Seus dados foram localizados.")
        
        # Exibe a posição em destaque
        st.metric(label="Sua Colocação Atual", value=f"{posicao}º Lugar")
            
    else:
        st.warning("CPF não encontrado. Certifique-se de que digitou corretamente.")

st.caption("🔒 Seus dados estão seguros. Este sistema não mostra sua posição para outros entregadores.")
