from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class FooterPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.save_button = QPushButton("Salvar Configuração")
        self.reset_button = QPushButton("Restaurar Padrões")

        layout.addWidget(self.save_button)
        layout.addWidget(self.reset_button)
        layout.addStretch()
