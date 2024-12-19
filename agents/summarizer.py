from langchain_openai import ChatOpenAI
from config.settings import settings

def summarize_documents(documents):
    """
    Gera resumos para uma lista de documentos.

    Args:
        documents (list): Lista de objetos Document.
    Returns:
        list: Lista de dicionários contendo a fonte e o resumo de cada documento.
    """
    if not documents:
        raise ValueError("Nenhum documento fornecido para sumarizar.")

    summaries = []
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=settings.openai_api_key)

    for doc in documents:
        try:
            response = llm.invoke(f"Resuma o seguinte texto:\n\n{doc.page_content}")
            summaries.append({"source": doc.metadata.get("source", "Desconhecida"), "summary": response.content})

        except Exception as e:
            print(f"Erro ao resumir o documento {doc.metadata.get('source', 'Desconhecida')}: {e}")
            summaries.append({"source": doc.metadata.get("source", "Desconhecida"), "summary": "Erro ao gerar o resumo."})

    return summaries
