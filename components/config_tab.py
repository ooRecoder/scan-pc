from PySide6.QtWidgets import QWidget, QHBoxLayout

from .service_sidebar import ServiceSidebar
from .service_content import ServiceContentArea

from core import ServiceManager, ConfigManager

class ConfigTab(QWidget):
    """Aba de configuração principal"""
    def __init__(self, service_manager: ServiceManager, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.service_manager = service_manager
        self.config_manager = config_manager
               
        # Create the main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)
        
        # Sidebar com serviços
        self.sidebar = ServiceSidebar(self.service_manager, self.config_manager)
        main_layout.addWidget(self.sidebar)
        
        # Área de conteúdo
        self.content_area = ServiceContentArea(self.service_manager)
        main_layout.addWidget(self.content_area, 1)
        
        # Conectar sinais
        self.sidebar.serviceSelected.connect(self.content_area.show_service)