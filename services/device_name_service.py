import platform
from .base_service import BaseService

class DeviceNameService(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        # Configurações padrão
        self.options.setdefault("include_hostname", True)   # nome do dispositivo
        self.options.setdefault("include_fqdn", False)      # nome de domínio completo

    def collect(self) -> dict:
        data = {}

        if self.options.get("include_hostname", True):
            data["Nome do dispositivo"] = platform.node()

        if self.options.get("include_fqdn", False):
            try:
                data["FQDN"] = platform.uname().node  # alternativa: socket.getfqdn()
            except Exception:
                data["FQDN"] = "Não disponível"

        return {"DeviceName": data}
