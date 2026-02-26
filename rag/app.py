import sys
import os
import streamlit as st

# Adiciona a pasta src ao caminho do Python para podermos importar nossos módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.generator import gerar_resposta

# Configuração da página
st.set_page_config(page_title="Meu RAG Local", page_icon="📚", layout="centered")

st.title("📚 Chat com meus PDFs (Qdrant + Gemini)")
st.markdown("Faça perguntas sobre os documentos que você ingeriu no banco vetorial.")

# Inicializa o histórico de chat na memória do Streamlit
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe o histórico de mensagens na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de texto para o usuário digitar a pergunta
if pergunta_usuario := st.chat_input("query: O que é pagged attention?"):
    
    # 1. Mostra a pergunta do usuário na tela e salva no histórico
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)
    st.session_state.mensagens.append({"role": "user", "content": pergunta_usuario})
    
    # 2. Mostra um spinner de carregamento enquanto o RAG trabalha
    with st.chat_message("assistant"):
        with st.spinner("Buscando nos documentos e gerando resposta..."):
            
            # Lembrete: Como o modelo E5 funciona melhor com o prefixo 'query:', 
            # nós o adicionamos aqui de forma invisível para o usuário!
            pergunta_formatada = f"query: {pergunta_usuario}"
            
            # Chama o nosso gerador!
            resposta_rag = gerar_resposta(pergunta_formatada)
            
            # Exibe a resposta
            st.markdown(resposta_rag)
            
    # 3. Salva a resposta do assistente no histórico
    st.session_state.mensagens.append({"role": "assistant", "content": resposta_rag})