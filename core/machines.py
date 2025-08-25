import json
import os
from typing import Dict, Any, Optional

class ComputerManager:
    """
    Gerencia os computadores scanneados e suas informações por serviço.
    """

    def __init__(self, file_path: str = "json/machines.json"):
        self.file_path = file_path
        self.computers: Dict[str, Dict[str, Any]] = {}
        self.load()

    def load(self):
        """Carrega os dados do arquivo JSON, se existir."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.computers = json.load(f)
        else:
            self.computers = {}

    def save(self):
        """Salva os dados atuais no arquivo JSON."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.computers, f, indent=4, ensure_ascii=False)

    def add_computer(self, identifier: str, data: Optional[Dict[str, Any]] = None):
        """
        Adiciona um computador pelo identificador (MAC, hostname, etc.)
        Se já existir, mantém os dados existentes ou atualiza se data for fornecido.
        """
        if data is None:
            data = {}
        if identifier not in self.computers:
            self.computers[identifier] = data
        else:
            self.computers[identifier].update(data)
        self.save()

    def remove_computer(self, identifier: str):
        """Remove um computador pelo identificador."""
        if identifier in self.computers:
            del self.computers[identifier]
            self.save()

    def get_computer(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Retorna os dados completos de um computador."""
        return self.computers.get(identifier)

    def get_service_data(self, identifier: str, service_name: str) -> Optional[Dict[str, Any]]:
        """Retorna os dados de um serviço específico de um computador."""
        computer = self.get_computer(identifier)
        if computer:
            return computer.get(service_name)
        return None

    def list_computers(self) -> list[str]:
        """Retorna a lista de identificadores de computadores."""
        return list(self.computers.keys())

    def update_service_data(self, identifier: str, service_name: str, service_data: Dict[str, Any]):
        """Atualiza ou adiciona dados de um serviço em um computador."""
        if identifier not in self.computers:
            self.computers[identifier] = {}
        self.computers[identifier][service_name] = service_data
        self.save()
