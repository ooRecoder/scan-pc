from abc import ABC, abstractmethod

class BaseService(ABC):
    """Classe base para todos os serviços."""

    @abstractmethod
    def collect(self) -> dict:
        """Cada serviço deve retornar um dicionário com os dados coletados."""
        pass
