# main.py
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (como a OPENROUTER_API_KEY)
load_dotenv()

# Importamos o construtor do nosso grafo
from src.graph import build_graph

def main():
    print("==================================================")
    print("🧠 Assistente de Pesquisa Multi-Agentes (IA)")
    print("==================================================\n")
    
    # 1. Definimos o tema da pesquisa
    topic = input("Qual tema de Inteligência Artificial você quer pesquisar? \n> ")
    
    # 2. Inicializamos o Estado Global com o tema
    initial_state = {
        "research_topic": topic,
        "plan": [],        # O Planner vai preencher isso
        "past_steps": [],  # O Executor vai preencher isso
        "final_report": "" # O Sintetizador vai preencher isso
    }
    
    # 3. Compilamos o grafo
    graph = build_graph()
    
    print("\n🚀 Iniciando os Agentes...\n")
    
    # 4. Executamos o fluxo em modo "stream" para vermos o progresso em tempo real
    # O config com recursion_limit garante que o loop do Executor não rode para sempre se der erro
    for output in graph.stream(initial_state, config={"recursion_limit": 15}):
        # Cada 'output' é um dicionário com o nome do nó que acabou de rodar e a atualização de estado
        for node_name, state_update in output.items():
            print(f"\n✅ Nó '{node_name}' finalizou sua tarefa.")
            
            # Se foi o planejador, mostramos o plano na tela
            if node_name == "planner":
                print("\n📋 Plano Estratégico Gerado:")
                for i, step in enumerate(state_update.get("plan", []), 1):
                    print(f"   {i}. {step}")
            print("-" * 50)

    # 5. O loop termina quando o 'synthesizer' roda. Vamos imprimir o resultado!
    # O último output sempre conterá o estado mais recente
    final_state = output.get("synthesizer", {})
    report = final_state.get("final_report", "Erro: Relatório não gerado.")
    
    print("\n==================================================")
    print("📄 RELATÓRIO FINAL")
    print("==================================================\n")
    print(report)

if __name__ == "__main__":
    main()