from doc_agent.graph.graph_builder import GraphBuilder

class GraphRunner:
    def __init__(self, vector_store):
        self.graph = GraphBuilder.build_graph(vector_store)

    def run(self, inputs):
        """
        Executa o grafo com os inputs fornecidos.

        Args:
            inputs (dict): Inputs contendo os documentos e a query.

        Returns:
            dict: Resultado do fluxo.
        """
        output = self.graph.run(inputs)
        return output
