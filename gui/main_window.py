from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel

from components import ConfigTab
from styles.styles import STYLESHEET
from core import ServiceManager, ConfigManager

class MainWindow(QMainWindow):
    def __init__(self, service_manager: ServiceManager, config_manager: ConfigManager):
        super().__init__()
        self.service_manager = service_manager
        self.setWindowTitle("Configuração de Serviços")
        self.setGeometry(100, 100, 1000, 700)
        
        # Aplicar estilos
        self.setStyleSheet(STYLESHEET)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(0)
        
        # Título principal
        title = QLabel("Configuração de Serviços")
        title.setObjectName("title")
        main_layout.addWidget(title)
        
        # Área principal com abas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Obter nomes dos serviços do ServiceManager
        service_names = self.service_manager.get_service_names()
        
        # Aba de configuração
        self.config_tab = ConfigTab(service_names, self.service_manager)
        self.tab_widget.addTab(self.config_tab, "Configuração")
        
        # Aba de verificação (placeholder)
        self.verify_tab = QWidget()
        self.tab_widget.addTab(self.verify_tab, "Verificação")