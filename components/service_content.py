from PySide6.QtWidgets import QStackedWidget, QWidget, QVBoxLayout, QLabel

class ServiceContentArea(QStackedWidget):
    """Área de conteúdo para configurações de serviços"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("contentArea")
        
        # Página inicial (vazia)
        self.initial_page = QWidget()
        initial_layout = QVBoxLayout(self.initial_page)
        initial_layout.addWidget(QLabel("Selecione um serviço para configurar"))
        self.addWidget(self.initial_page)