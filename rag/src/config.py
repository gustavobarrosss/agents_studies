import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# ==========================================
# CONFIGURAÇÕES DO BANCO VETORIAL (QDRANT)
# ==========================================
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "meu_primeiro_rag")

# ==========================================
# CONFIGURAÇÕES DO MODELO DE EMBEDDINGS
# ==========================================
# Vamos usar um modelo multilíngue do sentence_transformers que é leve,
# rápido e lida super bem com textos em Português!
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-small"

# ==========================================
# CAMINHOS DE PASTAS DO PROJETO
# ==========================================
# Pega o caminho absoluto da pasta raiz do projeto (uma pasta acima de 'src')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define a pasta onde os seus PDFs/Textos estão armazenados
DATA_DIR = os.path.join(BASE_DIR, "data")

# ==========================================
# CONFIGURAÇÕES DE CHUNKING (Divisão de texto)
# ==========================================
# Como os PDFs podem ser longos, precisamos quebrar em pedaços (chunks).
CHUNK_SIZE = 1000      # Quantidade de caracteres por pedaço
CHUNK_OVERLAP = 200     # Quantos caracteres se sobrepõem entre um pedaço e o próximo (mantém o contexto)