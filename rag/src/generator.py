import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Importamos a função de busca e o setup do banco do nosso retriever
from retriever import get_vector_store, buscar_com_filtro

def configurar_llm():
    """
    Configura e retorna o modelo de linguagem via OpenRouter.
    """
    print("🧠 Conectando ao modelo via OpenRouter...")
    
    # Pegamos a chave do nosso .env
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    
    # A sacada genial: Usamos a classe ChatOpenAI, mas mudamos a 'base_url'
    llm = ChatOpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        
        # Escolha o modelo que quiser! Abaixo estou usando o Llama 3 8B gratuito como exemplo.
        # Você pode trocar por "anthropic/claude-3-haiku", "openai/gpt-4o-mini", etc.
        model="openrouter/arcee-ai/trinity-large-preview:free", 
        
        temperature=0.1, # Mantemos baixo para evitar alucinações
        
        # A OpenRouter pede esses headers para identificar o seu app no painel deles
        default_headers={
            "HTTP-Referer": "http://localhost:8501", # URL de onde sua aplicação roda
            "X-Title": "Meu RAG Local", # Nome do seu app
        }
    )
    return llm

def gerar_resposta(pergunta):
    """
    Orquestra o RAG: Busca o contexto no banco e pede para o LLM responder.
    """
    vector_store = get_vector_store()
    
    print(f"🔍 Buscando contexto no Qdrant para: '{pergunta}'...")
    documentos_relevantes = buscar_com_filtro(
        vector_store=vector_store, 
        pergunta=pergunta, 
        k=3, 
        score_minimo=0.60 
    )
    
    if not documentos_relevantes:
        return "Desculpe, não encontrei informações suficientes na minha base de dados para responder a essa pergunta com precisão."
    
    # Extraímos apenas o texto
    textos_contexto = [doc.page_content for doc, score in documentos_relevantes]
    contexto_formatado = "\n\n---\n\n".join(textos_contexto)
    
    # O Prompt continua exatamente o mesmo!
    template_prompt = """
    Você é um assistente virtual especializado em responder perguntas com base APENAS nos documentos fornecidos.
    
    Abaixo estão os trechos de contexto recuperados da nossa base de conhecimento:
    <contexto>
    {contexto}
    </contexto>
    
    Responda à pergunta do usuário utilizando SOMENTE as informações do contexto acima.
    Se a resposta não estiver clara no contexto, diga que não sabe. 
    Responda em Português de forma clara e objetiva.
    
    Pergunta do Usuário: {pergunta}
    
    Resposta:
    """
    
    prompt = PromptTemplate(
        template=template_prompt,
        input_variables=["contexto", "pergunta"]
    )
    
    print("✍️ Gerando resposta com o LLM da OpenRouter...\n")
    llm = configurar_llm()
    
    prompt_final = prompt.format(contexto=contexto_formatado, pergunta=pergunta)
    resposta = llm.invoke(prompt_final)
    
    return resposta.content

if __name__ == "__main__":
    pergunta = "What is ReRoPe?"
    
    print("=" * 60)
    resposta_final = gerar_resposta(pergunta)
    print("🤖 RESPOSTA FINAL DO RAG:")
    print("-" * 60)
    print(resposta_final)
    print("=" * 60)