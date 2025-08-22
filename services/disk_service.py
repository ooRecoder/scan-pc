import psutil
from .base_service import BaseService

class DiskService(BaseService):
    def collect(self) -> dict:
        disks = {}
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            disks[part.device] = f"{round(usage.total / (1024**3), 2)} GB"
        return {"Discos": disks}
