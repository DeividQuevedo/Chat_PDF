from langgraph import Graph
from langgraph.node import Node
from agents.loader import DocumentLoader
from agents.summarizer import summarize_documents
from agents.retriever import DocumentRetriever
from agents.answer_generator import generate_answer

class GraphBuilder:
    """
    Configuração do grafo de agentes no LangGraph.
    """

    @staticmethod
    def build_graph(vector_store):
        graph = Graph()

        # Nós
        graph.add_node("load_documents", DocumentLoader.load_documents)
        graph.add_node("summarize_documents", summarize_documents)
        retriever = DocumentRetriever(vector_store)
        graph.add_node("retrieve_documents", retriever.retrieve)
        graph.add_node("generate_answer", generate_answer)

        # Conexões
        graph.add_edge("load_documents", "summarize_documents")
        graph.add_edge("summarize_documents", "retrieve_documents")
        graph.add_edge("retrieve_documents", "generate_answer")

        return graph
