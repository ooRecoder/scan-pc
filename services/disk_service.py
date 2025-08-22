import psutil
import platform
import subprocess
from shutil import which
import os
from .base_service import BaseService

class DiskService(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        # Configurações padrão
        self.options.setdefault("disk_type", True)
        self.options.setdefault("details", True)
        self.options.setdefault("io_stats", False)
        self.options.setdefault("usage", True)
        self.options.setdefault("health_check", False)  # nova opção

    # ------------------ Detecção de tipo de disco ------------------
    def _get_disk_type_windows(self, device):
        try:
            result = subprocess.check_output(
                ["wmic", "diskdrive", "get", "DeviceID,MediaType,Model,InterfaceType,SerialNumber,Manufacturer"],
                text=True
            )
            for line in result.splitlines():
                if device in line:
                    line_upper = line.upper()
                    tipo = "Desconhecido"
                    if "SSD" in line_upper:
                        tipo = "SSD"
                    elif "HDD" in line_upper or "FIXED" in line_upper:
                        tipo = "HDD"
                    elif "REMOVABLE" in line_upper:
                        tipo = "Pendrive/Removível"
                    detalhes = line.strip() if self.options.get("details") else ""
                    return {"Tipo": tipo if self.options.get("disk_type") else "Oculto", "Detalhes": detalhes}
            return {"Tipo": "Desconhecido", "Detalhes": ""}
        except Exception:
            return {"Tipo": "Desconhecido", "Detalhes": ""}

    def _get_disk_type_linux(self, device):
        try:
            dev = os.path.basename(device)
            tipo = "Desconhecido"

            # Tipo HDD/SSD
            path_rotational = f"/sys/block/{dev}/queue/rotational"
            if os.path.exists(path_rotational):
                with open(path_rotational, "r") as f:
                    tipo = "HDD" if f.read().strip() == "1" else "SSD"

            # Removível
            path_removable = f"/sys/block/{dev}/removable"
            if os.path.exists(path_removable):
                with open(path_removable, "r") as f:
                    if f.read().strip() == "1":
                        tipo = "Pendrive/Removível"

            # Modelo, fabricante, interface
            model = open(f"/sys/block/{dev}/device/model").read().strip() if os.path.exists(f"/sys/block/{dev}/device/model") else ""
            vendor = open(f"/sys/block/{dev}/device/vendor").read().strip() if os.path.exists(f"/sys/block/{dev}/device/vendor") else ""
            interface = open(f"/sys/block/{dev}/device/type").read().strip() if os.path.exists(f"/sys/block/{dev}/device/type") else ""
            detalhes = f"{vendor} {model} Interface: {interface}" if self.options.get("details") else ""

            return {"Tipo": tipo if self.options.get("disk_type") else "Oculto", "Detalhes": detalhes}
        except Exception:
            return {"Tipo": "Desconhecido", "Detalhes": ""}

    def _get_disk_type(self, device):
        if platform.system() == "Windows":
            return self._get_disk_type_windows(device)
        elif platform.system() == "Linux":
            return self._get_disk_type_linux(device)
        else:
            return {"Tipo": "Desconhecido", "Detalhes": ""}

    # ------------------ Saúde do disco (SMART) ------------------
    def _get_disk_health(self, device):
        if not self.options.get("health_check"):
            return "Não coletado"

        try:
            if platform.system() == "Windows":
                result = subprocess.check_output(
                    ["wmic", "diskdrive", "get", "Status,DeviceID"],
                    text=True
                )
                for line in result.splitlines():
                    if device in line:
                        status = line.replace(device, "").strip()
                        return status if status else "Desconhecido"
                return "Desconhecido"

            elif platform.system() == "Linux":
                if which("smartctl") is None:
                    return "smartctl não encontrado"

                # Executa smartctl e verifica return code
                result = subprocess.run(
                    ["smartctl", "-H", device],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    return f"Erro SMART (return code {result.returncode})"

                # Parse da saída
                for line in result.stdout.splitlines():
                    if "SMART overall-health self-assessment test result" in line:
                        return line.split(":")[-1].strip()
                return "Desconhecido"

        except Exception:
            return "Erro ao verificar saúde"

    # ------------------ Coleta de informações ------------------
    def collect(self) -> dict:
        discos = {}
        for part in psutil.disk_partitions(all=False):
            try:
                disco_info = {"Ponto de Montagem": part.mountpoint, "Sistema de Arquivos": part.fstype}

                # Tipo e detalhes
                if self.options.get("disk_type") or self.options.get("details"):
                    tipo_info = self._get_disk_type(part.device)
                    disco_info.update(tipo_info)

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

                # Saúde do disco (opcional)
                if self.options.get("health_check"):
                    saude = self._get_disk_health(part.device)
                    disco_info["Saúde"] = saude if saude is not None else "Não disponível"


                discos[part.device] = disco_info

            except PermissionError:
                continue
        return {"Discos": discos}
