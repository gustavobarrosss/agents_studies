# src/agents/executor.py
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.state import ResearchState
from src.tools.arxiv_search import search_arxiv

def executor_node(state: ResearchState):
    """
    Nó do Executor. Descobre qual é o próximo passo pendente, 
    chama o LLM equipado com ferramentas e executa a ação.
    """
    print("--- [EXECUTOR] Iniciando execução de tarefa ---")
    
    plan = state.get("plan", [])
    past_steps = state.get("past_steps", [])
    
    # 1. Descobrir qual é o passo atual
    # Se temos 0 passos concluidos, o index atual é 0 (o primeiro passo do plano).
    current_step_index = len(past_steps)
    
    # Proteção: se por acaso o executor for chamado quando tudo já acabou, não fazemos nada.
    if current_step_index >= len(plan):
        print("Todos os passos já foram executados!")
        return {"past_steps": []} 
        
    current_step = plan[current_step_index]
    print(f"Passo atual: {current_step}")
    
    # 2. Configurar o LLM via OpenRouter (mesma lógica do Planner)
    llm = ChatOpenAI(
        model="arcee-ai/trinity-large-preview:free", 
        temperature=0,
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    
    # 3. Vincular a ferramenta ao LLM
    # O método 'bind_tools' injeta a descrição da nossa função no LLM. 
    # É assim que o modelo sabe que PODE pesquisar na internet se precisar.
    llm_with_tools = llm.bind_tools([search_arxiv])
    
    # 4. Criar o prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um agente pesquisador operário. Sua única tarefa é completar O PASSO ATUAL do plano.\n"
                   "Sempre que precisar buscar papers, use a ferramenta 'search_arxiv'.\n"
                   "Tema geral da pesquisa: {topic}"),
        ("user", "Execute este passo: {step}")
    ])
    
    chain = prompt | llm_with_tools
    
    # 5. O LLM avalia o passo e decide se usa a ferramenta ou responde direto
    response = chain.invoke({
        "topic": state["research_topic"],
        "step": current_step
    })
    
    result_text = ""
    
    # 6. Lógica de execução da ferramenta
    # Se o LLM decidiu usar a ferramenta, a propriedade 'tool_calls' virá preenchida
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "search_arxiv":
                # Extraímos os argumentos (a query de busca) que o LLM gerou sozinho
                args = tool_call["args"]
                print(f"[*] O LLM acionou a ferramenta search_arxiv com a query: {args}")
                
                # Executamos a função Python real que criamos no passo anterior
                tool_result = search_arxiv.invoke(args)
                result_text += f"Resultado da busca:\n{tool_result}\n"
    else:
        # Se o LLM achou que não precisava da ferramenta, pegamos apenas o texto gerado
        print("[*] O LLM respondeu sem usar ferramentas.")
        result_text = response.content
        
    # 7. Retornar a atualização do Estado
    # Lembramos que lá no state.py usamos o 'operator.add'.
    # Portanto, retornar essa lista de 1 tupla fará o LangGraph ADICIONAR 
    # este resultado ao final do histórico 'past_steps'.
    return {"past_steps": [(current_step, result_text)]}