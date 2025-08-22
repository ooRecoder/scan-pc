import platform
from .base_service import BaseService

class OSService(BaseService):
    def collect(self) -> dict:
        return {
            "Sistema Operacional": platform.system(),
            "Versão": platform.version(),
            "Release": platform.release()
        }
