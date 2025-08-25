from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .service_checkbox import ServiceCheckBox

class ServiceSidebar(QScrollArea):
    """Barra lateral com lista de serviços"""
    def __init__(self, service_names, parent=None):
        super().__init__(parent)
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
        self.service_checkboxes = {}
        for service in service_names:
            cb = ServiceCheckBox(service)
            cb.setCursor(Qt.CursorShape.PointingHandCursor)
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