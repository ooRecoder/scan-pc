import platform
from .base_service import BaseService

class CPUService(BaseService):
    def collect(self) -> dict:
        return {"CPU": platform.processor()}
