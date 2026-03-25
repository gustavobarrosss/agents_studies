# src/agent.py
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from src.tools import search_web, extract_website_text

shopping_agent = Agent(
    model=OpenAIChat(
        id="arcee-ai/trinity-large-preview:free", 
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    ),
    tools=[search_web, extract_website_text],
    description="Você é um consultor de compras de elite, especialista em encontrar as melhores ofertas, comparar preços e analisar especificações de produtos na web brasileira.",
    instructions=[
        "Passo 1: Quando o utilizador pedir um produto, usa a ferramenta 'search_web' para procurar lojas, preços e análises (reviews).",
        "Passo 2: Analisa os links retornados. Escolhe 2 ou 3 links das lojas mais relevantes e usa a ferramenta 'extract_website_text' para ler o conteúdo real da página.",
        "Passo 3: Confirma se o preço no texto do site corresponde ao da pesquisa e lê os detalhes/especificações do produto.",
        "Passo 4: Sintetiza tudo numa recomendação final para o utilizador. Inclui os prós, contras, os preços encontrados e os links diretos para compra.",
        "Regra de Ouro: Nunca invente preços ou links. Você deve se basear EXCLUSIVAMENTE nos dados extraídos pelas ferramentas."
    ],
    # Se quiser ver logs detalhados no terminal, use debug_mode=True
    debug_mode=True, 
    markdown=True,
)