from abc import ABC, abstractmethod

class BaseService(ABC):
    """Classe base para todos os serviços."""

    def __init__(self, **options):
        # cada serviço pode receber parâmetros específicos
        self.options = options  

    @abstractmethod
    def collect(self) -> dict:
        raise NotImplementedError("Cada serviço deve implementar o método collect")
