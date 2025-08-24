from core.scanner import Scanner

if __name__ == "__main__":
    print("=== Machine Scanner ===")

    config = {
        "CPUService": {"usage": True},
        "DiskService": {"detail": "full"},
        "RAMService": {},
        "OSService": {}
    }

    scanner = Scanner(config)

    # Executa o scan e salva no JSON
    results = scanner.run()

    print("\n=== Resultado do Scan (runtime) ===")
    for k, v in results.items():
        print(f"{k}: {v}")

    print("\n=== Informações salvas no JSON ===")
    saved = scanner.get_saved_info()
    for k, v in saved.items():
        print(f"{k}: {v}")
