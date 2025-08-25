from core.scanner import Scanner

if __name__ == "__main__":
    print("=== Machine Scanner ===")

    scanner = Scanner({"Bios"})

    # Executa o scan e salva no JSON
    results = scanner.run()
