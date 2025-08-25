# scanner.py
import importlib
from core.config_manager import ConfigManager
from core.storage import update_machine_info, get_machine_info

class Scanner:
    def __init__(self, services):
        self.config_manager = ConfigManager()
        self.services = services  # Lista de nomes dos serviços

    def run(self, save=True):
        results = {}
        for service_name in self.services:
            module = importlib.import_module(f"services.{service_name.lower()}_service")
            service_class = getattr(module, service_name.upper())
            options = self.config_manager.get_service_config(service_name)
            service_instance = service_class(**options)
            
            results.update(service_instance.collect())
            
            if save:
                update_machine_info(results)  # <--- Salva no JSON

        return results

    def get_saved_info(self):
        """Retorna as informações salvas desta máquina."""
        return get_machine_info()