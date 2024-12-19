import streamlit as st
from pathlib import Path
from tempfile import NamedTemporaryFile
from agents.loader import DocumentLoader
from agents.summarizer import summarize_documents
from agents.retriever import DocumentRetriever
from agents.answer_generator import generate_answer
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.chat_history import InMemoryChatMessageHistory

# Configuração da página
st.set_page_config(page_title="Agente de Documentos", layout="centered")

# Inicializar estados na sessão
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = InMemoryChatMessageHistory()

if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None

if "documents" not in st.session_state:
    st.session_state["documents"] = []

if "summarization_sent" not in st.session_state:
    st.session_state["summarization_sent"] = False

if "temp_summary_file" not in st.session_state:
    st.session_state["temp_summary_file"] = None


# Funções auxiliares
def process_uploaded_files(uploaded_files):
    """Processa os arquivos enviados pelo usuário."""
    temp_dir = Path("temp_files")
    temp_dir.mkdir(exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = temp_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    # Carregar e processar documentos
    st.session_state["documents"] = DocumentLoader.load_documents(str(temp_dir))
    st.success("Documentos carregados e processados com sucesso!")

    # Criar embeddings e vector store
    embeddings = OpenAIEmbeddings()
    st.session_state["vector_store"] = FAISS.from_documents(
        st.session_state["documents"], embeddings
    )
    st.success("Vector Store criada com sucesso!")

    # Gerar sumarização inicial
    summaries = summarize_documents(st.session_state["documents"])
    combined_summary = " ".join([summary["summary"] for summary in summaries])

    # Armazenar sumarização em arquivo temporário
    with NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(combined_summary)
        st.session_state["temp_summary_file"] = tmp_file.name

    if not st.session_state["summarization_sent"]:
        st.session_state["chat_history"].add_message(
            {"role": "assistant", "content": f"Foram carregados {len(st.session_state['documents'])} documentos contendo informações sobre \"{combined_summary}\". O que você gostaria de saber sobre esses documentos?"}
        )
        st.session_state["summarization_sent"] = True


def update_secondary_summary(query, answer):
    """Atualiza a segunda sumarização incrementalmente no arquivo temporário."""
    with open(st.session_state["temp_summary_file"], "a") as f:
        f.write(f"\n\nUsuário: {query}\nAssistente: {answer}")


def build_chat_interface():
    """Renderiza a interface do chat."""
    st.subheader("Chat Interativo")
    for message in st.session_state["chat_history"].messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    user_input = st.chat_input("Digite sua pergunta:")
    if user_input:
        # Adicionar mensagem do usuário ao chat
        st.session_state["chat_history"].add_message({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if st.session_state["vector_store"]:
            retriever = DocumentRetriever(st.session_state["vector_store"])
            results = retriever.retrieve(user_input)

            # Carregar contexto incremental do arquivo temporário e histórico do chat
            with open(st.session_state["temp_summary_file"], "r") as f:
                temp_summary = f.read()

            chat_context = "\n".join(
                [msg["content"] for msg in st.session_state["chat_history"].messages]
            )

            full_context = f"{temp_summary}\n\nHistórico do Chat:\n{chat_context}"

            # Gera resposta
            answer = generate_answer(results, user_input, full_context)
            if not answer:
                answer = f"Sinto muito, não encontrei informações sobre \"{user_input}\" nos documentos carregados!"

            # Adicionar resposta ao chat
            st.session_state["chat_history"].add_message({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

            # Atualizar segunda sumarização
            update_secondary_summary(user_input, answer)


# Página principal
def build_page():
    """Renderiza a aplicação principal."""
    with st.sidebar:
        st.header("Upload de Documentos")
        uploaded_files = st.file_uploader(
            "Envie seus arquivos:", type=["txt", "pdf", "docx"], accept_multiple_files=True
        )
        if uploaded_files:
            process_uploaded_files(uploaded_files)

    build_chat_interface()


# Executar a página
if __name__ == "__main__":
    build_page()
