import platform
from .base_service import BaseService

class OSService(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        # Configurações padrão
        self.options.setdefault("system", True)   # Mostrar nome do SO
        self.options.setdefault("version", True)  # Mostrar versão
        self.options.setdefault("release", True)  # Mostrar release

    def collect(self) -> dict:
        data = {}

        if self.options.get("system", True):
            data["Sistema Operacional"] = platform.system()

        if self.options.get("version", True):
            data["Versão"] = platform.version()

        if self.options.get("release", True):
            data["Release"] = platform.release()

        return {"S.O": data}
