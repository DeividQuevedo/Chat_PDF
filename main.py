from agents.loader import DocumentLoader
from agents.summarizer import summarize_documents
from agents.retriever import DocumentRetriever
from agents.answer_generator import generate_answer
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

import os

def main():
    # Configurações iniciais
    folder_path = "data/example_documents"
    query = "Resumo do documento ou informações relevantes"

    print("=== 1. Carregando Documentos ===")
    # Carregar documentos
    try:
        documents = DocumentLoader.load_documents(folder_path)
        print(f"{len(documents)} documentos carregados com sucesso.\n")
    except Exception as e:
        print(f"Erro ao carregar documentos: {e}")
        return

    print("=== 2. Gerando Embeddings e Criando Vector Store ===")
    # Criar embeddings e vector store
    try:
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(documents, embeddings)
        print("Vector Store criado com sucesso.\n")
    except Exception as e:
        print(f"Erro ao criar o Vector Store: {e}")
        return

    print("=== 3. Sumarizando Documentos ===")
    # Gerar resumos
    try:
        summaries = summarize_documents(documents)
        for summary in summaries:
            print(f"Fonte: {summary['source']}")
            print(f"Resumo: {summary['summary']}\n")
    except Exception as e:
        print(f"Erro ao gerar resumos: {e}")
        return

    print("=== 4. Recuperando Documentos e Gerando Respostas ===")
    # Recuperar documentos relevantes e gerar resposta
    try:
        retriever = DocumentRetriever(vector_store)
        results = retriever.retrieve(query)

        if results:
            print("Documentos Recuperados:")
            for doc in results:
                print(f"- {doc.page_content[:100]}...\n")

            # Gerar resposta
            answer = generate_answer(results, query)
            print(f"Resposta:\n{answer}")
        else:
            print("Nenhum documento relevante foi encontrado.")
    except Exception as e:
        print(f"Erro ao buscar documentos ou gerar resposta: {e}")

if __name__ == "__main__":
    main()
