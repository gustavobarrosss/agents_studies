# src/state.py
import operator
from typing import Annotated, List, TypedDict

class ResearchState(TypedDict):
    """
    Define a 'memória' compartilhada do nosso sistema multi-agentes.
    O LangGraph passa esse dicionário de nó em nó.
    """
    
    # O tópico que o usuário quer pesquisar. Ex: "RAG em LLMs 2024"
    research_topic: str
    
    # O plano gerado pelo agente Planejador. É uma lista de strings.
    plan: List[str]
    
    # O histórico do que já foi executado.
    # IMPORTANTE: O `Annotated` e o `operator.add` são comandos do LangGraph.
    # Sem isso, cada vez que o Executor salvasse um resultado, ele apagaria o anterior.
    # O `operator.add` diz ao LangGraph: "Quando receber um novo dado aqui, faça um append na lista".
    # Usamos uma lista de tuplas para guardar (nome_do_passo, resultado_do_passo).
    past_steps: Annotated[List[tuple], operator.add]
    
    # A síntese final, que será entregue ao usuário no final do processo.
    final_report: str