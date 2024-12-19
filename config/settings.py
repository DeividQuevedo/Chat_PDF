import os
import yaml

class Config:
    """Gerencia configurações do projeto."""

    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        self.openai_api_key = self.load_api_key()

    def load_api_key(self):
        """Carrega a chave OpenAI da variável de ambiente ou do arquivo config.yaml."""
        # Prioridade para variáveis de ambiente
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key:
            return api_key

        # Se a variável de ambiente não existir, tenta carregar do arquivo config.yaml
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                return config.get("OPENAI_API_KEY")

        # Retorna None se a chave não estiver disponível
        print("Aviso: Nenhuma chave OpenAI disponível. Algumas funcionalidades podem não funcionar.")
        return None


# Instanciar a configuração
settings = Config()

# Exemplo de uso
if settings.openai_api_key:
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
