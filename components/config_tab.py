from PySide6.QtWidgets import QWidget, QHBoxLayout

from .service_sidebar import ServiceSidebar
from .service_content import ServiceContentArea

class ConfigTab(QWidget):
    """Aba de configuração principal"""
    def __init__(self, service_names, sm, parent=None):
        super().__init__(parent)
        
        # Create the main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(16)
        
        # Sidebar com serviços
        self.sidebar = ServiceSidebar(service_names)
        main_layout.addWidget(self.sidebar)
        
        # Área de conteúdo
        self.content_area = ServiceContentArea()
        main_layout.addWidget(self.content_area, 1)  # Expande para preencher espaço