import platform, psutil
from .base_service import BaseService

class CPUService(BaseService):
    def collect(self) -> dict:
        include_usage = self.options.get("usage", False)
        data = {"CPU": platform.processor()}
        
        if include_usage:
            data["Uso (%)"] = f"{psutil.cpu_percent(interval=1)}"
            data["Núcleos"] = f"{psutil.cpu_count(logical=True)}"

        return data
