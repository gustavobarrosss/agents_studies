# src/tools/arxiv_search.py
import arxiv
from langchain_core.tools import tool

# O decorador @tool é a mágica do LangChain/LangGraph. 
# Ele transforma uma função Python comum em algo que o LLM consegue "enxergar" e usar.
@tool
def search_arxiv(query: str, max_results: int = 3) -> str:
    """
    Busca artigos acadêmicos e papers no arXiv com base em uma string de consulta (query).
    Retorna um resumo formatado contendo o título, autores, data de publicação e o abstract do paper.
    Use esta ferramenta sempre que precisar de informações reais e atualizadas sobre artigos de IA.
    """
    print(f"--- [FERRAMENTA] Buscando no arXiv por: '{query}' ---")
    
    # Instanciamos o cliente da API do arXiv
    client = arxiv.Client()
    
    # Criamos o objeto de busca configurando a query, a quantidade de resultados 
    # e ordenando pela relevância do artigo.
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    # Lista para armazenar os resultados formatados
    results_list = []
    
    try:
        # Executamos a busca e iteramos sobre cada paper encontrado
        for paper in client.results(search):
            # Formatamos os autores separando por vírgula
            authors = ", ".join([author.name for author in paper.authors])
            
            # Montamos um bloco de texto estruturado para cada paper
            paper_info = (
                f"Título: {paper.title}\n"
                f"Autores: {authors}\n"
                f"Publicado em: {paper.published.strftime('%Y-%m-%d')}\n"
                f"URL: {paper.pdf_url}\n"
                f"Resumo (Abstract): {paper.summary}\n"
                "--------------------------------------------------"
            )
            results_list.append(paper_info)
            
        # Se a busca não retornar nada, avisamos o LLM para que ele não alucine
        if not results_list:
            return f"Nenhum artigo encontrado no arXiv para a busca: {query}."
            
        # Juntamos todos os papers em uma única string de texto para o LLM ler
        return "\n".join(results_list)
        
    except Exception as e:
        # É crucial capturar erros na ferramenta para que o agente não "quebre" (crash).
        # Em vez disso, retornamos o erro como texto para o LLM, para que ele saiba
        # que a busca falhou e possa tentar outra estratégia se necessário.
        return f"Erro ao buscar no arXiv: {str(e)}"