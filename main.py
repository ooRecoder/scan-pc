import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from core import ServiceManager

def main():
    sm = ServiceManager()
    # Criar aplicação
    app = QApplication(sys.argv)     
    # Criar janela principal
    window = MainWindow(service_manager=sm)
    window.show()
    # Executar aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()