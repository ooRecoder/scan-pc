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
        :return: dict com 'Modelo' e 'Detalhes'
        """
        if not drive_letter.endswith("\\"):
            drive_letter += "\\"
        
        c = wmi.WMI()
        
        for disk in c.Win32_DiskDrive():
            for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    if logical_disk.DeviceID.upper() == drive_letter.rstrip("\\").upper():
                        # Converter o objeto WMI em dicionário
                        detalhes = {prop: getattr(disk, prop) for prop in disk.properties.keys()}
                        return {
                            "Modelo": disk.Model,
                            "Status": disk.Status,
                            "Detalhes": detalhes
                        }
        
        return {
            "Modelo": None,
            "Status": None,
            "Detalhes": {}
        }

    # ------------------ Coleta de informações ------------------
    def collect(self) -> dict:
        discos = {}
        for part in psutil.disk_partitions(all=False):
            try:
                disco_info = {
                    "Ponto de Montagem": part.mountpoint,
                    "Sistema de Arquivos": part.fstype
                }

                # Tipo e detalhes
                if self.options.get("disk_model"):
                    info = self._get_disk_info(part.device)
                    disco_info["Modelo"] = info.get("Modelo", "")
                    disco_info["Status"] = info.get("Status", "Desconhecido")
                    # disco_info["Detalhes"] = info.get("Detalhes", {})

                # Uso
                if self.options.get("usage"):
                    usage = psutil.disk_usage(part.mountpoint)
                    disco_info.update({
                        "Total": f"{round(usage.total / (1024**3), 2)} GB",
                        "Usado": f"{round(usage.used / (1024**3), 2)} GB",
                        "Livre": f"{round(usage.free / (1024**3), 2)} GB",
                        "Percentual": f"{usage.percent}%"
                    })

                # Estatísticas de IO
                if self.options.get("io_stats"):
                    io_stats = psutil.disk_io_counters(perdisk=True).get(os.path.basename(part.device), None)
                    if io_stats:
                        disco_info["IO"] = (
                            f"Lidos: {io_stats.read_bytes}, Gravados: {io_stats.write_bytes}, "
                            f"Leituras: {io_stats.read_count}, Gravações: {io_stats.write_count}"
                        )
                    else:
                        disco_info["IO"] = "Não disponível"

                discos[part.device] = disco_info

            except PermissionError:
                continue
        return {"Discos": discos}
