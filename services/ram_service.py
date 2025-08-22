import psutil
from .base_service import BaseService

class RAMService(BaseService):
    def collect(self) -> dict:
        return {"RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"}
