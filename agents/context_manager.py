from tempfile import NamedTemporaryFile

class ContextManager:
    """Gerencia o contexto incremental de conversas."""

    def __init__(self):
        self.context_file = NamedTemporaryFile(mode="w+", delete=False, suffix=".txt")
        self.initialized = False

    def initialize_context(self, summary):
        if not self.initialized:
            self.context_file.write(summary + "\n")
            self.context_file.flush()
            self.initialized = True

    def append_context(self, user_query, response):
        """Atualiza o contexto com a pergunta e resposta."""
        self.context_file.write(f"Usuário: {user_query}\nAssistente: {response}\n")
        self.context_file.flush()

    def get_context(self):
        """Recupera o contexto atual."""
        self.context_file.seek(0)
        return self.context_file.read()
