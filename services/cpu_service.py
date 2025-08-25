import platform
import psutil
from .base_service import BaseService

class CPU(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        # Configurações padrão
        self.options.setdefault("usage", False)   # mostrar uso da CPU
        self.options.setdefault("cores", True)    # mostrar número de núcleos
        self.options.setdefault("details", True)  # mostrar detalhes do processador

    def collect(self) -> dict:
        data = {}

        if self.options.get("details", True):
            data["CPU"] = platform.processor()

        if self.options.get("usage", True):
            data["Usage (%)"] = psutil.cpu_percent(interval=1)

        if self.options.get("cores", True):
            data["Cores"] = psutil.cpu_count(logical=True)

        return {"CPU": data}
