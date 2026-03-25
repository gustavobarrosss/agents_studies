# main.py
import os
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env (crucial para a chave da API funcionar)
load_dotenv()

# 2. Importa o nosso agente já configurado com as ferramentas e o prompt
from src.agent import shopping_agent

def main():
    print("=======================================================")
    print("🛒 Consultor de Compras Autônomo (ReAct via Agno)")
    print("=======================================================\n")
    print("Dica: Peça para buscar um produto, comparar preços")
    print("ou encontrar a melhor oferta. Digite 'sair' para encerrar.\n")

    # 3. Criamos um loop infinito para manter a conversa ativa
    while True:
        # Pega a entrada do usuário
        user_query = input("Você: ")
        
        # Condição de parada do programa
        if user_query.lower() in ['sair', 'exit', 'quit']:
            print("\nEncerrando o consultor. Boas compras!")
            break
            
        # Evita que o programa quebre se o usuário apertar 'Enter' sem digitar nada
        if not user_query.strip():
            continue
            
        print("\n🤖 Consultor iniciando o raciocínio...\n")
        
        # 4. A Mágica do Agno: Execução e Streaming
        # O método 'print_response' faz tudo sozinho:
        # - Mostra no terminal quais ferramentas estão sendo chamadas
        # - Exibe a resposta final do LLM fluindo na tela (stream=True)
        # - Formata tudo em Markdown bonitinho
        shopping_agent.print_response(user_query, stream=True)
        
        print("\n" + "="*55 + "\n")

if __name__ == "__main__":
    main()