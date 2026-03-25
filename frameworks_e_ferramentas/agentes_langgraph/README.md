# Auditoria de Segurança com LangGraph

Sistema de auditoria automatizada de repositórios GitHub, construído com LangGraph. Demonstra o padrão **Fan-Out/Fan-In**: após clonar o repositório, três agentes de análise rodam em paralelo e seus resultados são consolidados por um agregador.

## Agentes

- **fetch_repo**: Clona o repositório remoto localmente para análise.
- **sast_scan**: Realiza análise estática do código (SAST - Static Application Security Testing).
- **sca_scan**: Verifica dependências vulneráveis (SCA - Software Composition Analysis).
- **docs_analysis**: Analisa a documentação em busca de informações sensíveis ou lacunas.
- **aggregator**: Consolida os resultados dos três agentes e gera o relatório final.

## Fluxo

```
fetch_repo --> sast_scan    ---|
           --> sca_scan     ---|--> aggregator --> END
           --> docs_analysis---|
```

## Como executar

```bash
cd frameworks_e_ferramentas/agentes_langgraph
python main.py
```

O URL do repositório é definido diretamente em `main.py` na variável `test_repo`.
