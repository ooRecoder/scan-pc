import platform
from .base_service import BaseService

class DeviceNameService(BaseService):
    def collect(self) -> dict:
        return {"Nome do dispositivo": platform.node()}
