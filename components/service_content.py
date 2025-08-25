from PySide6.QtWidgets import QStackedWidget, QWidget, QVBoxLayout, QLabel

class ServiceContentArea(QStackedWidget):
    """Área de conteúdo para configurações de serviços"""
    def __init__(self, service_manager, parent=None):
        super().__init__(parent)
        self.service_manager = service_manager
        self.setObjectName("contentArea")
        
        # Página inicial (vazia)
        self.initial_page = QWidget()
        initial_layout = QVBoxLayout(self.initial_page)
        initial_layout.addWidget(QLabel("Selecione um serviço para configurar"))
        self.addWidget(self.initial_page)
        
        # Criar páginas para cada serviço
        self.service_pages = {}
        for service_name in self.service_manager.get_service_names():
            self.add_service_page(service_name)
    
    def add_service_page(self, service_name):
        """Adiciona uma página de configuração para um serviço"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Título do serviço
        title = QLabel(service_name)
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Descrição do serviço
        description = self.service_manager.get_service_description(service_name)
        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # TODO: Adicionar widgets para as opções do serviço
        # baseado no tipo de cada opção (checkbox, dropdown, etc.)
        
        layout.addStretch()
        self.addWidget(page)
        self.service_pages[service_name] = page