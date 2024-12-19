from langchain_openai import ChatOpenAI
from config.settings import settings

def generate_answer(retrieved_docs, query, chat_context):
    """
    Gera uma resposta com base nos documentos recuperados, na query e no contexto do chat.

    Args:
        retrieved_docs (list): Documentos recuperados.
        query (str): Pergunta do usuário.
        chat_context (str): Histórico do chat.

    Returns:
        str: Resposta gerada.
    """
    if not retrieved_docs:
        return f"Sinto muito, não encontrei informações sobre \"{query}\" nos documentos carregados!"

    combined_docs = "\n\n".join([doc.page_content for doc in retrieved_docs])
    prompt = f"""
    Você é um assistente que responde exclusivamente com base nos documentos e no histórico fornecido.

    Histórico do Chat:
    {chat_context}

    Documentos:
    {combined_docs}

    Pergunta:
    {query}

    Se a resposta não puder ser encontrada nos documentos fornecidos, responda:
    "Sinto muito, não encontrei informações sobre \"{query}\" nos documentos carregados!"
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=settings.openai_api_key)
  


    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"
