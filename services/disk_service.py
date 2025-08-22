import psutil
import platform
import subprocess
import os
from .base_service import BaseService

class DiskService(BaseService):
    def _get_disk_type_windows(self, device):
        """Detecta tipo de disco no Windows usando WMIC"""
        try:
            result = subprocess.check_output(
                ["wmic", "diskdrive", "get", "DeviceID,MediaType"],
                text=True
            )
            for line in result.splitlines():
                if device in line:
                    if "SSD" in line.upper():
                        return "SSD"
                    elif "HDD" in line.upper() or "FIXED" in line.upper():
                        return "HDD"
                    elif "REMOVABLE" in line.upper():
                        return "Pendrive/Removível"
            return "Desconhecido"
        except Exception:
            return "Desconhecido"

    def _get_disk_type_linux(self, device):
        """Detecta tipo de disco no Linux via /sys/block"""
        try:
            dev = os.path.basename(device)
            path = f"/sys/block/{dev}/queue/rotational"
            if os.path.exists(path):
                with open(path, "r") as f:
                    rotational = f.read().strip()
                    return "HDD" if rotational == "1" else "SSD"

            removable_path = f"/sys/block/{dev}/removable"
            if os.path.exists(removable_path):
                with open(removable_path, "r") as f:
                    if f.read().strip() == "1":
                        return "Pendrive/Removível"

            return "Desconhecido"
        except Exception:
            return "Desconhecido"

    def _get_disk_type(self, device):
        if platform.system() == "Windows":
            return self._get_disk_type_windows(device)
        elif platform.system() == "Linux":
            return self._get_disk_type_linux(device)
        else:
            return "Desconhecido"

    def collect(self) -> dict:
        discos = {}
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                tipo = self._get_disk_type(part.device)

                discos[part.device] = {
                    "Tipo": tipo,
                    "Total": f"{round(usage.total / (1024**3), 2)} GB",
                    "Usado": f"{round(usage.used / (1024**3), 2)} GB",
                    "Livre": f"{round(usage.free / (1024**3), 2)} GB",
                    "Percentual": f"{usage.percent}%"
                }
            except PermissionError:
                continue
        return {"Discos": discos}
