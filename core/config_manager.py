import json
import os

CONFIG_FILE = "json/config.json"

class ConfigManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.config = {}
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_service_config(self, service_name):
        # Retorna config de um serviço, com fallback vazio
        return self.config.get(service_name, {})

    def set_service_config(self, service_name, options):
        self.config[service_name] = options
        self.save()

    def list_services(self):
        return list(self.config.keys())
