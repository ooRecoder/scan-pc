from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

class ServicePanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Scroll para opções
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)

        scroll.setWidget(self.content)

        # Exemplo de placeholder
        self.content_layout.addWidget(QLabel("Selecione um serviço para configurar"))

        layout.addWidget(scroll)

    def load_service(self, service_name: str, options: dict):
        """
        Carrega dinamicamente as opções do serviço.
        Será implementado depois com checkboxes/combobox etc.
        """
        pass
