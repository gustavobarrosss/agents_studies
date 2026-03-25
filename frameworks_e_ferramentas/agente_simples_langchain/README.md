# Agente de Vendas com LangChain

Agente de atendimento ao cliente da loja fictícia "TechFlow", construído com LangChain usando o padrão ReAct (Reasoning + Acting). Demonstra a criação de um agente com ferramentas personalizadas, memória de conversa e estrutura modular.

## Ferramentas

- **Busca de Produtos**: Fuzzy search sobre o catálogo da loja. Funciona mesmo com nomes incompletos.
- **Calculo de Imposto**: Executa calculos matematicos via codigo para evitar erros do LLM.

## Estrutura

```
src/
├── agents/     # Criacao do agente e executor
├── tools/      # Ferramentas personalizadas
├── prompts/    # System prompts
└── utils/      # Configuracao da API e helpers
```

## Como executar

```bash
cd frameworks_e_ferramentas/agente_simples_langchain
python -m src.main
```

Obrigatorio rodar com `-m src.main` a partir da pasta do projeto, nao via `python src/main.py`.

Requer `OPENAI_API_KEY` e `OPENAI_API_BASE` no `.env` (configurados para OpenRouter).
