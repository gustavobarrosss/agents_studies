# src/graph.py
import os
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Importamos nossos módulos
from src.state import ResearchState
from src.agents.planner import planner_node
from src.agents.executor import executor_node

# --- 1. Nó Sintetizador (Para gerar o relatório final) ---
def synthesizer_node(state: ResearchState):
    """
    Nó final. Pega o tema original e todo o histórico de execução (past_steps)
    e redige um relatório final organizado.
    """
    print("--- [SINTETIZADOR] Escrevendo o relatório final ---")
    
    # Configuramos o LLM via OpenRouter
    llm = ChatOpenAI(
        model="arcee-ai/trinity-large-preview:free", 
        temperature=0.3,
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    
    # Preparamos o histórico formatado para o LLM ler
    history_text = ""
    for step_name, result in state.get("past_steps", []):
        history_text += f"Passo: {step_name}\nResultado:\n{result}\n\n"
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um redator técnico especialista em Inteligência Artificial. "
                   "Sua tarefa é ler as anotações de pesquisa de um assistente operário e "
                   "escrever um relatório final coeso, bem formatado em Markdown.\n"
                   "Observações: Redija esse relatório em Português Brasileiro"
                   "Esse relatório deve conter TUDO que alguém precisa para entender o tema, independente de seu tamanho e complexidade"
                   "Gere esse relatório em um nível decrescente de abstração, ou seja, comece com a conceituação e vá aprofundando"
                   "Tema original: {topic}"),
        ("user", "Anotações da pesquisa:\n{history}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "topic": state["research_topic"],
        "history": history_text
    })
    
    # Atualizamos o campo final_report no nosso Estado
    return {"final_report": response.content}


# --- 2. Função de Roteamento (A Bússola do Grafo) ---
def route_executor(state: ResearchState) -> str:
    """
    Esta função decide para onde o grafo deve ir depois que o Executor roda.
    Se ainda há passos no plano, volta para o Executor. 
    Se não, vai para o Sintetizador.
    """
    plan = state.get("plan", [])
    past_steps = state.get("past_steps", [])
    
    # Se o número de passos executados for menor que o total do plano, continua executando
    if len(past_steps) < len(plan):
        print(f"--- [ROTEADOR] Passo {len(past_steps)} concluído. Voltando para o Executor... ---")
        return "executor" # Retorna o nome do próximo nó
    else:
        print("--- [ROTEADOR] Plano concluído. Indo para a síntese... ---")
        return "synthesizer"


# --- 3. Construção do Grafo ---
def build_graph():
    """
    Monta e compila o LangGraph.
    """
    # Iniciamos o grafo passando o nosso ResearchState como modelo de memória
    workflow = StateGraph(ResearchState)
    
    # Adicionamos os nós (damos um nome em string e passamos a função correspondente)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("synthesizer", synthesizer_node)
    
    # Definimos o fluxo principal (as arestas normais)
    workflow.add_edge(START, "planner") # Do início, vai para o planejador
    workflow.add_edge("planner", "executor") # Do planejador, vai para o executor
    
    # Definimos a aresta condicional (o loop)
    # Dizemos: "Saindo do 'executor', rode a função 'route_executor'. 
    # Dependendo da resposta dela, vá para o 'executor' ou para o 'synthesizer'."
    workflow.add_conditional_edges(
        "executor",
        route_executor,
        {
            "executor": "executor",       # Se route_executor retornar "executor", vai para "executor"
            "synthesizer": "synthesizer"  # Se retornar "synthesizer", vai para "synthesizer"
        }
    )
    
    # Aresta final
    workflow.add_edge("synthesizer", END)
    
    # Compilamos o grafo para que ele fique pronto para uso
    return workflow.compile()