# src/tools.py
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 5) -> str:
    """
    Faz uma busca na internet para encontrar produtos, lojas e preços.
    Retorna uma lista de resultados contendo o título da página, o link (URL) e um breve resumo.
    """
    print(f"\n🔍 [FERRAMENTA] Buscando na web por: '{query}'...")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "Nenhum resultado encontrado na web para esta busca."
            
        formatted_results = ""
        for i, res in enumerate(results, 1):
            formatted_results += (
                f"{i}. Título: {res['title']}\n"
                f"   Link: {res['href']}\n"
                f"   Resumo: {res['body']}\n\n"
            )
        return formatted_results
        
    except Exception as e:
        return f"Erro ao realizar a busca: {str(e)}"


def extract_website_text(url: str) -> str:
    """
    Acessa uma URL específica e extrai todo o texto limpo da página.
    Use o link (href) retornado pela ferramenta 'search_web' aqui.
    """
    print(f"\n📄 [FERRAMENTA] Tentando ler o site: {url}...")
    
    # "Disfarce" para o site achar que somos um usuário normal usando o Google Chrome no Windows
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        # TIMEOUT DE 10 SEGUNDOS: A regra de ouro de agentes resilientes. 
        # Se o Mercado Livre bloquear, o bot desiste rápido em vez de travar o terminal.
        response = requests.get(url, headers=headers, timeout=10)
        
        # Se o site der erro 403 (Proibido) ou 404 (Não encontrado), cai no except
        response.raise_for_status() 
        
        # Extrai o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts e estilos CSS que poluem o texto
        for script in soup(["script", "style"]):
            script.extract()
            
        # Pega só o texto visível
        text = soup.get_text(separator=' ', strip=True)
        
        # Limita a 5000 caracteres para não sobrecarregar o cérebro (LLM) do agente
        return f"Conteúdo extraído da página:\n{text[:5000]}"
        
    except requests.exceptions.Timeout:
        return f"Erro: O site {url} demorou muito para responder (Timeout). Tente outro link."
    except Exception as e:
        return f"Erro ao acessar {url} (Possível bloqueio anti-bot do e-commerce): {str(e)}"