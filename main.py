import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from core import ServiceManager, ConfigManager

def main():
    sm = ServiceManager()
    cm = ConfigManager("json/config.json")
    # Criar aplicação
    app = QApplication(sys.argv)     
    # Criar janela principal
    window = MainWindow(service_manager=sm, config_manager=cm)
    window.show()
    # Executar aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()