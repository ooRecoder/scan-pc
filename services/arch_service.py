import platform
from .base_service import BaseService

class ArchService(BaseService):
    def collect(self) -> dict:
        arch, _ = platform.architecture()
        return {"Arquitetura": arch}
