import streamlit as st
import pandas as pd

# 1. Configuração da página (deve ser o primeiro comando do Streamlit)
st.set_page_config(page_title="Ranking de Entregadores", page_icon="🛵", layout="centered")

# 2. Função para carregar o arquivo Excel/CSV do ranking
@st.cache_data
def carregar_dados():
    # Substitua 'ranking.csv' pelo nome real do seu arquivo.
    # O comando dtype={'cpf': str} é fundamental para não estragar CPFs que começam com 0
    df = pd.read_csv("ranking.csv", dtype={'cpf': str})
    
    # IMPORTANTE: Se a sua planilha já tiver uma coluna de posição/ranking, 
    # você não precisa da linha abaixo. Se não tiver, o Python calcula para você:
    if 'Posição' not in df.columns:
        df['Posição'] = df['pontuacao'].rank(ascending=False, method='min').astype(int)
        
    return df

try:
    df_ranking = carregar_dados()
except FileNotFoundError:
    st.error("Erro: O arquivo 'ranking.csv' não foi encontrado na mesma pasta do código.")
    st.stop()

# 3. Interface Visual do Usuário
st.title("🛵 Consulta de Ranking - Entregadores")
st.write("Insira seu CPF abaixo para verificar sua pontuação e colocação atual.")

# Campo de texto para o entregador digitar
cpf_digitado = st.text_input("Digite seu CPF (apenas números):", max_chars=14)

# 4. Lógica de Busca Oculta
if cpf_digitado:
    # Limpa o que o usuário digitou tirando espaços, pontos e traços
    cpf_limpo = cpf_digitado.strip().replace(".", "").replace("-", "")
    
    # Limpa também a coluna de CPF da planilha para garantir que a comparação funcione
    df_ranking['cpf_limpo'] = df_ranking['cpf'].astype(str).str.replace(".", "", regex=False).str.replace("-", "", regex=False).str.strip()
    
    # Faz o filtro (PROCV do Streamlit)
    resultado = df_ranking[df_ranking['cpf_limpo'] == cpf_limpo]
    
    if not resultado.empty:
        # Puxa as informações da linha encontrada
        nome = resultado.iloc[0]['Entregador'] # Mude para o nome exato da sua coluna de nomes
        posicao = resultado.iloc[0]['Posição']
        
        # Se você tiver coluna de pontuação/entregas, pode puxar aqui:
        # pontos = resultado.iloc[0]['pontuacao'] 
        
        st.success(f"Olá, **{nome}**! Seus dados foram localizados.")
        
        # Exibe em um formato de destaque (cartão de métrica)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Sua Colocação Atual", value=f"{posicao}º Lugar")
        # with col2:
        #     st.metric(label="Total de Pontos/Entregas", value=f"{pontos}")
            
    else:
        st.warning("CPF não encontrado. Certifique-se de que digitou corretamente ou se você está cadastrado nesta rodada do ranking.")

# Nota de rodapé sobre privacidade
st.caption("🔒 Seus dados estão seguros. Este sistema não mostra sua posição para outros entregadores.")