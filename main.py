import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    # Criar aplicação
    app = QApplication(sys.argv)    
    # Criar janela principal
    window = MainWindow()
    window.show()
    # Executar aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()