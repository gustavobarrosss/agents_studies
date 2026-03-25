# Analista de Investimentos com CrewAI

Sistema multiagente para análise de ações da bolsa de valores, construído com CrewAI em processo sequencial. Demonstra a criação de times de agentes com papéis e tarefas definidas via arquivos YAML.

## Agentes

- **Researcher**: Coleta dados técnicos da ação via API de mercado.
- **Validator**: Revisa e valida os dados coletados pelo Researcher e pelo News Analyst.
- **News Analyst**: Busca e analisa notícias recentes e sentimento de mercado.
- **Investment Advisor**: Consolida todas as análises e gera a recomendação final.

## Fluxo

```
researcher -> validator -> news_analyst -> validator -> investment_advisor
```

## Como executar

```bash
cd frameworks_e_ferramentas/multi_agentes_crewAI
python main.py
```

O ticker da ação é definido em `main.py` na variável `ticket` (padrão: `PETR4.SA`). O relatório final é salvo em `relatorios/`.
