import platform
from .base_service import BaseService

class DeviceNameService(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        
    def collect(self) -> dict:
        return {"Nome do dispositivo": platform.node()}
