import platform
import psutil
from .base_service import BaseService

class CPUService(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        # Configurações padrão
        self.options.setdefault("usage", True)   # mostrar uso da CPU
        self.options.setdefault("cores", True)   # mostrar número de núcleos
        self.options.setdefault("details", True) # mostrar detalhes do processador

    def collect(self) -> dict:
        data = {}

        if self.options.get("details", True):
            data["CPU"] = platform.processor()

        if self.options.get("usage", True):
            data["Uso (%)"] = psutil.cpu_percent(interval=1)

        if self.options.get("cores", True):
            data["Núcleos"] = psutil.cpu_count(logical=True)

        return data
