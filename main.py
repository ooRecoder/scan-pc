from core.scanner import Scanner
from core.storage import get_machine_info

if __name__ == "__main__":
    config = {
        "CPUService": {"usage": True},
        "DiskService": {"detail": "full"},
        "RAMService": {},
        "OSService": {}
    }

    scanner = Scanner(config)
    resultado = scanner.run()

    print("=== Resultado do Scan ===")
    for k, v in resultado.items():
        print(f"{k}: {v}")

    print("\n=== Dados salvos no JSON ===")
    print(get_machine_info())
