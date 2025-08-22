from services.cpu_service import CPUService
from services.disk_service import DiskService
from services.ram_service import RAMService
from services.os_service import OSService
from services.arch_service import ArchService
from services.device_name_service import DeviceNameService

class Scanner:
    def __init__(self, config=None):
        """
        config = {
            "CPUService": {"usage": True},
            "DiskService": {"detail": "full"},
            "RAMService": {},
            "OSService": {}
        }
        """
        self.config = config or {}

        # Instancia serviços com base nas configs
        self.services = []
        for service_class in [OSService, CPUService, RAMService, DiskService, ArchService, DeviceNameService]:
            name = service_class.__name__
            options = self.config.get(name, {})
            self.services.append(service_class(**options))

    def run(self):
        results = {}
        for service in self.services:
            results.update(service.collect())
        return results
