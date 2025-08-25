import json
import os

CONFIG_FILE = "json/config.json"

class ConfigManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.config = {}
        self.load()

    def load(self):
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.config = {}
        else:
            self.config = {}

    def save(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get_service_config(self, service_name):
        # Retorna None se o serviço não existe, ou o dict de configuração (pode ser vazio {})
        return self.config.get(service_name)

    def set_service_config(self, service_name, options):
        self.config[service_name] = options
        self.save()
        
    def remove_service(self, service_name):
        if service_name in self.config:
            del self.config[service_name]
            self.save()

    def list_services(self):
        return list(self.config.keys())
    
    def get_all_configs(self):
        return self.config.copy()
    
    def update_service_option(self, service_name, option_name, value):
        """Atualiza uma opção específica de um serviço"""
        if service_name not in self.config:
            self.config[service_name] = {}
        self.config[service_name][option_name] = value
        self.save()
    
    def get_service_option(self, service_name, option_name, default=None):
        """Obtém o valor de uma opção específica de um serviço"""
        service_config = self.get_service_config(service_name)
        if service_config is None:
            return default
        return service_config.get(option_name, default)