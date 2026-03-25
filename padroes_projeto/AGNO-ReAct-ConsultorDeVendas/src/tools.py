# src/tools.py
from duckduckgo_search import DDGS
from newspaper import Article

def search_web(query: str, max_results: int = 5) -> str:
    """
    Faz uma busca na internet para encontrar produtos, lojas e preços.
    Retorna uma lista de resultados contendo o título da página, o link (URL) e um breve resumo.
    Sempre use esta ferramenta primeiro para encontrar onde o produto está sendo vendido.
    """
    print(f"\n🔍 [FERRAMENTA] Buscando na web por: '{query}'...")
    
    try:
        # Iniciamos o cliente do DuckDuckGo
        with DDGS() as ddgs:
            # Fazemos a busca pedindo apenas texto e limitando os resultados
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "Nenhum resultado encontrado na web para esta busca."
            
        # Formatamos a saída para o LLM entender facilmente
        formatted_results = ""
        for i, res in enumerate(results, 1):
            formatted_results += (
                f"{i}. Título: {res['title']}\n"
                f"   Link: {res['href']}\n"
                f"   Resumo: {res['body']}\n\n"
            )
        
        return formatted_results
        
    except Exception as e:
        # Sempre retornamos o erro em texto para não quebrar o agente
        return f"Erro ao realizar a busca: {str(e)}"


def extract_website_text(url: str) -> str:
    """
    Acessa uma URL específica e extrai todo o texto limpo da página.
    Use o link (href) retornado pela ferramenta 'search_web' aqui.
    Esta ferramenta é crucial para ler os detalhes técnicos do produto e confirmar o preço real na loja.
    """
    print(f"\n📄 [FERRAMENTA] Lendo conteúdo do site: {url}...")
    
    try:
        # A biblioteca newspaper3k baixa e limpa o HTML, extraindo apenas o artigo/texto principal
        article = Article(url)
        article.download()
        article.parse()
        
        # Opcional, mas recomendado: pegar as palavras-chave principais do site
        article.nlp() 
        
        # Limitamos o texto aos primeiros 6000 caracteres. 
        # Isso é vital porque sites de e-commerce têm muito código inútil no HTML 
        # e não queremos estourar o limite de tokens (memória) do nosso LLM.
        clean_text = article.text[:6000] 
        
        return (
            f"Título da Página: {article.title}\n"
            f"Palavras-chave: {', '.join(article.keywords)}\n"
            f"Conteúdo:\n{clean_text}"
        )
        
    except Exception as e:
        return f"Erro ao extrair dados do site {url}: {str(e)}"