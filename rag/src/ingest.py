import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

# Importamos as configurações que criamos no passo anterior
from config import (
    DATA_DIR, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP, 
    EMBEDDING_MODEL_NAME,
    QDRANT_HOST,
    QDRANT_PORT,
    COLLECTION_NAME
)


def ingest_documents():
    print("Iniciando o processo de ingestão de dados...")

    # 1. CARREGAMENTO DOS DOCUMENTOS
    print(f"Lendo PDFs da pasta: {DATA_DIR}")
    # O PyPDFDirectoryLoader vai procurar por todos os arquivos .pdf dentro da pasta data/
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    
    if not documents:
        print("Nenhum documento PDF encontrado na pasta data/.")
        return

    print(f"{len(documents)} páginas carregadas com sucesso.")

    # 2. DIVISÃO DO TEXTO (CHUNKING)
    print(f" Dividindo o texto em pedaços de {CHUNK_SIZE} caracteres...")
    # O RecursiveCharacterTextSplitter tenta quebrar o texto respeitando parágrafos e frases
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""] # Ordem de preferência de onde cortar
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Texto dividido em {len(chunks)} pedaços (chunks).")

    # 3. CONFIGURAÇÃO DO MODELO DE EMBEDDINGS LOCAL
    print(f"🧠 Carregando modelo de embeddings local: {EMBEDDING_MODEL_NAME}...")
    # Na primeira vez que rodar, ele vai baixar o modelo da internet. Depois, usará o cache.
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # 4. SALVANDO NO QDRANT
    print("💾 Gerando vetores e salvando no Qdrant...")
    # Montamos a URL de conexão com o Qdrant local
    qdrant_url = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
    
    # Esta função faz a mágica acontecer: 
    # Calcula os embeddings de todos os chunks e envia para o Qdrant.
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=qdrant_url,
        collection_name=COLLECTION_NAME,
        force_recreate=True # ATENÇÃO: True apaga a coleção anterior se existir e cria uma nova. Ideal para testes.
    )

    print("🎉 Ingestão concluída com sucesso! Seus dados estão no Qdrant.")

if __name__ == "__main__":
    # Verifica se a pasta data existe, se não, cria para evitar erros
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"⚠️ A pasta {DATA_DIR} foi criada. Coloque seus PDFs lá e rode novamente.")
    else:
        ingest_documents()