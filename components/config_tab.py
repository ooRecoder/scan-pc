from PySide6.QtWidgets import QWidget, QHBoxLayout

from .service_sidebar import ServiceSidebar
from .service_content import ServiceContentArea

class ConfigTab(QWidget):
    """Aba de configuração principal"""
    def __init__(self, service_names, service_manager, parent=None):
        super().__init__(parent)
        self.service_manager = service_manager
        
        # Create the main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)
        
        # Sidebar com serviços
        self.sidebar = ServiceSidebar(service_names, self.service_manager)
        main_layout.addWidget(self.sidebar)
        
        # Área de conteúdo
        self.content_area = ServiceContentArea(self.service_manager)
        main_layout.addWidget(self.content_area, 1)  # Expande para preencher espaço