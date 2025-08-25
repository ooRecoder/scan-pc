# scanner.py
import importlib
from core.config_manager import ConfigManager
from core.storage import update_machine_info, get_machine_info

class Scanner:
    def __init__(self):
        self.config_manager = ConfigManager()

    def run(self, save=True):
        results = {}

        # Pega todos os serviços habilitados na config
        enabled_services = list(self.config_manager.config.keys())

        for service_name in enabled_services:
            try:
                # Importa módulo dinamicamente
                module = importlib.import_module(f"services.{service_name.lower()}_service")
                service_class = getattr(module, service_name.upper())
                # Pega opções do config.json
                options = self.config_manager.get_service_config(service_name)
                service_instance = service_class(**options)

                # Executa coleta
                results.update(service_instance.collect())

                # Salva os dados
                if save:
                    update_machine_info(results)

            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Erro ao executar serviço {service_name}: {e}")

        return results

    def get_saved_info(self):
        """Retorna as informações salvas desta máquina."""
        return get_machine_info()
