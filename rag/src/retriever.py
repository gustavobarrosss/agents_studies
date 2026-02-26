from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from config import (
    QDRANT_HOST,
    QDRANT_PORT,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME
)

def get_vector_store():
    print("🔍 Conectando ao Qdrant...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    qdrant_url = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
    client = QdrantClient(url=qdrant_url)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    return vector_store

def buscar_com_filtro(vector_store, pergunta, k=3, score_minimo=0.65):
    """
    Busca documentos, mas só retorna aqueles que atingem a nota de corte.
    """
    resultados_brutos = vector_store.similarity_search_with_score(pergunta, k=k)
    resultados_filtrados = []
    
    for doc, score in resultados_brutos:
        if score >= score_minimo:
            resultados_filtrados.append((doc, score))
            
    return resultados_filtrados

if __name__ == "__main__":
    vector_store = get_vector_store()
    
    pergunta_teste = "query:What is ReRoPe?"
    print(f"\nTeste de busca para a pergunta: '{pergunta_teste}'")
    print("="*60)
    
    # Em vez de usar o 'as_retriever', vamos usar a busca com Score para investigar!
    # No Qdrant (usando Cosine), o score vai de 0.0 a 1.0. (Mais próximo de 1.0 é melhor).
    documentos_encontrados = vector_store.similarity_search_with_score(pergunta_teste, k=3)
    
    for i, (doc, score) in enumerate(documentos_encontrados):
        print(f"\n--- 📄 RESULTADO {i+1} | SCORE DE SIMILARIDADE: {score:.4f} ---")
        # Mostramos os primeiros 150 caracteres para não poluir a tela
        print(doc.page_content.strip()[:150] + "...")
        print("-" * 60)