# Pesquisador de IA com LangGraph (Planner-Executor)

Assistente de pesquisa acadêmica que gera relatórios sobre temas de Inteligência Artificial. Implementa o padrão Planner-Executor com LangGraph: o Planejador cria um roteiro de pesquisa e o Executor percorre cada passo buscando papers no Arxiv.

## Agentes

- **Planner**: Recebe o tema e gera um plano de pesquisa estruturado de 3 a 5 passos.
- **Executor**: Percorre o plano passo a passo, buscando papers relevantes no Arxiv via ferramenta.
- **Synthesizer**: Consolida todos os resultados e gera o relatório final em markdown.

## Fluxo

```
planner --> executor (loop) --> synthesizer --> END
                ^_____________|
```

O loop do executor continua enquanto houver passos pendentes no plano.

## Saída

O relatório final é exportado como PDF na pasta `relatorios/`.

## Como executar

```bash
cd padroes_projeto/LANGGRAPH-PLANNER-EXECUTOR-PesquisadorDeIA
python main.py
```

Requer `OPENROUTER_API_KEY` no `.env`.
