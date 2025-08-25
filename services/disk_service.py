import psutil
import subprocess
import os
import wmi  # precisa instalar: pip install wmi
from .base_service import BaseService


class DiskService(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        # Configurações padrão
        self.options.setdefault("disk_model", True)
        self.options.setdefault("details", True)
        self.options.setdefault("io_stats", False)
        self.options.setdefault("usage", True)
        self.options.setdefault("health_check", False)  # nova opção

    # ------------------ Detecta modelo e detalhes do disco ------------------
    def _get_disk_info(self, drive_letter):
        """
        Retorna o modelo da unidade e todos os detalhes do disco.
        
        :param drive_letter: Letra da unidade, ex: 'C:\\'
        :return: dict com 'Model' e 'Details'
        """
        if not drive_letter.endswith("\\"):
            drive_letter += "\\"
        
        c = wmi.WMI()
        
        for disk in c.Win32_DiskDrive():
            for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    if logical_disk.DeviceID.upper() == drive_letter.rstrip("\\").upper():
                        # Converter o objeto WMI em dicionário
                        details = {prop: getattr(disk, prop) for prop in disk.properties.keys()}
                        return {
                            "Model": disk.Model,
                            "Status": disk.Status,
                            "Details": details
                        }
        
        return {
            "Model": None,
            "Status": None,
            "Details": {}
        }

    # ------------------ Coleta de informações ------------------
    def collect(self) -> dict:
        disks = {}
        for part in psutil.disk_partitions(all=False):
            try:
                disk_info = {
                    "MountPoint": part.mountpoint,
                    "FileSystem": part.fstype
                }

                # Tipo e detalhes
                if self.options.get("disk_model"):
                    info = self._get_disk_info(part.device)
                    disk_info["Model"] = info.get("Model", "")
                    disk_info["Status"] = info.get("Status", "Unknown")
                    # disk_info["Details"] = info.get("Details", {})

                # Uso
                if self.options.get("usage"):
                    usage = psutil.disk_usage(part.mountpoint)
                    disk_info.update({
                        "Total": f"{round(usage.total / (1024**3), 2)} GB",
                        "Used": f"{round(usage.used / (1024**3), 2)} GB",
                        "Free": f"{round(usage.free / (1024**3), 2)} GB",
                        "Percent": f"{usage.percent}%"
                    })

                # Estatísticas de IO
                if self.options.get("io_stats"):
                    io_stats = psutil.disk_io_counters(perdisk=True).get(os.path.basename(part.device), None)
                    if io_stats:
                        disk_info["IO"] = (
                            f"Read: {io_stats.read_bytes}, Written: {io_stats.write_bytes}, "
                            f"Reads: {io_stats.read_count}, Writes: {io_stats.write_count}"
                        )
                    else:
                        disk_info["IO"] = "Not available"

                disks[part.device] = disk_info

            except PermissionError:
                continue
        return {"Disks": disks}
