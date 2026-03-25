# Consultor de Compras com AGNO (ReAct)

Agente de compras autônomo que busca produtos, compara preços e extrai informações diretamente de e-commerces brasileiros. Construído com o framework AGNO e demonstra o padrão ReAct aplicado a web scraping.

## Ferramentas

- **search_web**: Realiza buscas no DuckDuckGo por produtos, preços e lojas.
- **extract_website_text**: Acessa URLs e extrai o conteúdo textual da página com BeautifulSoup.

## Fluxo

O agente recebe a query do usuário, busca lojas e preços na web, acessa as páginas mais relevantes para confirmar os dados e retorna uma recomendação com preços e links diretos. Nunca inventa dados — tudo vem das ferramentas.

## Como executar

```bash
cd padroes_projeto/AGNO-ReAct-ConsultorDeVendas
python main.py
```

Requer `OPENROUTER_API_KEY` no `.env`.
