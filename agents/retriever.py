from langchain_community.vectorstores import FAISS

class DocumentRetriever:
    """
    Agente responsável por buscar documentos relevantes no vector store.
    """
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query, k=3):
        """
        Recupera os documentos mais relevantes para uma query.

        Args:
            query (str): A query fornecida pelo usuário.
            k (int): Número de documentos relevantes a retornar.

        Returns:
            list: Lista de documentos relevantes.
        """
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Erro ao buscar documentos: {e}")
            return []
