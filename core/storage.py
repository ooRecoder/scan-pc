import json
from pathlib import Path
from typing import Any, Dict, Optional
from core.utils import get_mac_address

DATA_FILE = Path("json/machines.json")


def load_data() -> Dict[str, Any]:
    """Carrega os dados do arquivo JSON."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data: Dict[str, Any]) -> None:
    """Salva os dados completos no JSON."""
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def update_machine_info(new_info: Dict[str, Any]) -> None:
    """
    Atualiza as informações da máquina atual no JSON.
    Se já existe, mescla os dados em vez de sobrescrever tudo.
    """
    mac = get_mac_address()
    data = load_data()

    if mac not in data:
        data[mac] = {}

    # Faz merge: sobrescreve apenas as chaves novas/alteradas
    data[mac].update(new_info)

    save_data(data)

def get_machine_info(mac: Optional[str] = None) -> Dict[str, Any]:
    """
    Retorna as informações de uma máquina específica.
    Se não for passado MAC, retorna a máquina atual.
    """
    data = load_data()
    if mac is None:
        mac = get_mac_address()
    return data.get(mac, {})
