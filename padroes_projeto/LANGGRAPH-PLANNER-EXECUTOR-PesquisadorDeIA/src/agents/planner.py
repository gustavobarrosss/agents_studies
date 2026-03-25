# src/agents/planner.py
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 
from pydantic import BaseModel, Field
from src.state import ResearchState

# 1. Definindo o "Contrato" de saída do LLM
class Plan(BaseModel):
    """Esquema Pydantic que força o LLM a retornar estritamente uma lista de passos."""
    steps: list[str] = Field(
        description="Lista de passos detalhados para pesquisar o tema. Cada passo deve ser uma ação de busca ou leitura."
    )

# 2. Criando a função que atua como o Nó (Node) no LangGraph
def planner_node(state: ResearchState):
    """
    Nó do Planejador. Recebe o estado atual, lê o tema e gera um plano.
    """
    print("--- [PLANEJADOR] Criando o plano de pesquisa ---")
    
    topic = state["research_topic"]
    
    # Instanciando o LLM via OpenRouter
    # IMPORTANTE: Você precisará colocar OPENROUTER_API_KEY no seu arquivo .env
    llm = ChatOpenAI(
        model="arcee-ai/trinity-large-preview:free", # No OpenRouter, o formato é sempre 'provedor/modelo' (ex: anthropic/claude-3.5-sonnet)
        temperature=0.1,
        api_key=os.environ.get("OPENROUTER_API_KEY"), 
        base_url="https://openrouter.ai/api/v1" # Aqui fazemos o "desvio" da OpenAI para o OpenRouter
    )
    
    # Forçamos o LLM a responder exclusivamente no formato da classe 'Plan'
    structured_llm = llm.with_structured_output(Plan)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente de pesquisa acadêmica sênior especializado em Inteligência Artificial. "
                   "Sua tarefa é receber um tema e criar um plano de pesquisa direto e focado de 3 a 5 passos. "
                   "Os passos devem ser em nível crescente de complexidade e detalhamento. Ou seja, da conceituação até o detalhamento a nível baixo de abstração."
                   "Garanta que seu plano englobe tudo sobre o tema pesquisado, para até um leigo no assunto conseguir ser um especialista depois de cumprir os passos."
                   "Não adicione passos desnecessários."),
        ("user", "Crie um plano de pesquisa para o seguinte tema: {research_topic}")
    ])
    
    planner_chain = prompt | structured_llm
    
    # Executamos a requisição
    response = planner_chain.invoke({"research_topic": topic})
    
    # Retornamos o dicionário atualizando apenas o campo "plan" no estado global
    return {"plan": response.steps}