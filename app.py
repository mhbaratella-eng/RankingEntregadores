import streamlit as st
import pandas as pd

# 1. Configuração da página (deve ser o primeiro comando)
st.set_page_config(page_title="Ranking de Entregadores", page_icon="🛵", layout="centered")

# 2. Função para carregar e padronizar os dados da planilha
@st.cache_data
def carregar_dados():
    # Carrega o CSV mapeando tudo inicialmente como texto
    df = pd.read_csv("ranking.csv", dtype=str)
    
    # PADRONIZAÇÃO DE SEGURANÇA:
    # Remove espaços invisíveis e transforma todos os nomes de colunas em minúsculo.
    # Assim, 'CPF', 'cpf ', 'Cpf' viram apenas 'cpf'.
    df.columns = df.columns.str.strip().str.lower()
    
    return df

try:
    df_ranking = carregar_dados()
except FileNotFoundError:
    st.error("Erro: O arquivo 'ranking.csv' não foi encontrado no seu repositório do GitHub.")
    st.stop()

# 3. Interface Visual do Usuário
st.title("🛵 Consulta de Ranking - Entregadores")
st.write("Insira seu CPF abaixo para verificar sua colocação atual.")

# Campo para o entregador digitar o CPF
cpf_digitado = st.text_input("Digite seu CPF (apenas números):", max_chars=14)

# 4. Lógica de Busca e Exibição Oculta
if cpf_digitado:
    # 4.1 Limpa pontos e traços que o usuário possa ter digitado no campo
    cpf_limpo = cpf_digitado.strip().replace(".", "").replace("-", "")
    
    # 4.2 Limpa e padroniza a coluna de CPF da planilha para a comparação funcionar
    if 'cpf' in df_ranking.columns:
        df_ranking['cpf_limpo'] = df_ranking['cpf'].astype(str).str.replace(".", "", regex=False).str.replace("-", "", regex=False).str.strip()
        
        # Faz o filtro (procura o CPF digitado na planilha)
        resultado = df_ranking[df_ranking['cpf_limpo'] == cpf_limpo]
        
        if not resultado.empty:
            # Puxa os dados usando os nomes das colunas já padronizados em minúsculo
            nome = resultado.iloc[0]['entregador']
            posicao = resultado.iloc[0]['posição']
            
            # Mensagem de sucesso para o entregador
            st.success(f"Olá, **{nome}**! Seus dados foram localizados.")
            
            # Exibe a posição em um cartão de destaque grande
            st.metric(label="Sua Colocação Atual", value=f"{posicao}º Lugar")
                
        else:
            st.warning("CPF não encontrado. Certifique-se de que digitou corretamente.")
            
    else:
        st.error("Erro técnico: Não encontramos a coluna 'cpf' na sua planilha. Verifique o arquivo ranking.csv.")

# Nota de rodapé sobre privacidade dos dados
st.caption("🔒 Seus dados estão seguros. Este sistema não mostra sua posição para outros entregadores.")
