# RAG com Qdrant e OpenRouter

Sistema de perguntas e respostas sobre documentos PDF locais. Utiliza Qdrant como banco vetorial, modelo de embeddings local (HuggingFace E5) e LLM via OpenRouter para geração de respostas. A interface é construída com Streamlit.

## Pipeline

**Ingestão** (`src/ingest.py`): Carrega PDFs da pasta `data/`, divide em chunks, gera embeddings com o modelo E5 e armazena no Qdrant local.

**Consulta** (`app.py`): Recebe a pergunta do usuário, busca os chunks mais relevantes no Qdrant por similaridade e envia o contexto junto com a pergunta ao LLM para gerar a resposta.

## Como executar

**1. Ingerir documentos** (apenas na primeira vez ou ao adicionar PDFs):

```bash
# Coloque seus PDFs em rag/data/
python src/ingest.py
```

**2. Iniciar a interface**:

```bash
cd rag
streamlit run app.py
```

Requer Qdrant rodando localmente (`localhost:6333`) e `OPENROUTER_API_KEY` no `.env`.
