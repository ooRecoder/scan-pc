from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .service_checkbox import ServiceCheckBox
from core import ServiceManager, ConfigManager

class ServiceSidebar(QScrollArea):
    """Barra lateral com lista de serviços"""
    serviceSelected = Signal(str)
    
    def __init__(self, service_manager: ServiceManager, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        
        self.service_manager = service_manager
        self.config_manager = config_manager
        
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedWidth(250)
        
        # Widget de container
        container = QWidget()
        container.setObjectName("sidebar")
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título
        title = QLabel("Serviços Disponíveis")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title.setFont(title_font)
        title.setStyleSheet("color: #2d3748; margin: 12px 0;")
        layout.addWidget(title)
        
        # Checkboxes para serviços
        service_names = self.service_manager.get_service_names()
        self.service_checkboxes = {}
        for service in service_names:
            cb = ServiceCheckBox(service)
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
            
            # Obter descrição do serviço
            description = self.service_manager.get_service_description(service)
            if description:
                cb.setToolTip(description)
            
            # Verificar se o serviço está na configuração (considera que está ativo se existe na config)
            service_exists_in_config = service in self.config_manager.config
            if service_exists_in_config:
                cb.setChecked(True)
            
            # Conectar sinal de foco para mostrar detalhes
            cb.focused.connect(self.serviceSelected.emit)
            
            # Conectar clique para mostrar detalhes e atualizar configuração
            cb.stateChanged.connect(lambda state, s=service: self.on_service_selected(s, state))
            
            self.service_checkboxes[service] = cb
            layout.addWidget(cb)
        
        # Espaçador
        layout.addStretch()
        
        # Botão de ação
        self.run_button = QPushButton("Executar Serviços")
        self.run_button.setObjectName("primaryButton")
        self.run_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.run_button)
        
        self.setWidget(container)
    
    def on_service_selected(self, service_name, state):
        """Lida com a seleção de um serviço"""
        if state == Qt.CheckState.Checked.value:
            # Se o serviço foi selecionado, garantir que existe na configuração
            service_config = self.config_manager.get_service_config(service_name)
            if not service_config:
                # Se não existe configuração, criar uma vazia
                self.config_manager.set_service_config(service_name, {})
            
            self.serviceSelected.emit(service_name)
        else:
            # Se o serviço foi deselecionado, remover da configuração
            self.config_manager.remove_service(service_name)