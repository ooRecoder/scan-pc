from services.cpu_service import CPUService
from services.disk_service import DiskService
from services.ram_service import RAMService
from services.os_service import OSService
from services.device_model_service import DeviceInfoService
from services.bios_service import BiosService
from core.storage import update_machine_info, get_machine_info


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
        for service_class in [OSService, CPUService, RAMService,
                              DiskService, DeviceInfoService, BiosService]:
            name = service_class.__name__
            options = self.config.get(name, {})
            self.services.append(service_class(**options))

    def run(self, save=True):
        results = {}
        for service in self.services:
            results.update(service.collect())

        if save:
            update_machine_info(results)  # <--- Salva no JSON

        return results

    def get_saved_info(self):
        """Retorna as informações salvas desta máquina."""
        return get_machine_info()

