from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter, QVBoxLayout
from PySide6.QtCore import Qt
from gui.service_list import ServiceList
from gui.service_panel import ServicePanel
from gui.footer_panel import FooterPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Service Configurator")
        self.setGeometry(200, 200, 900, 600)

        # Layout principal
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Splitter com lista de serviços e painel de opções
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.service_list = ServiceList()
        self.service_panel = ServicePanel()

        splitter.addWidget(self.service_list)
        splitter.addWidget(self.service_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        # Rodapé com botões
        self.footer = FooterPanel()

        # Adiciona ao layout principal
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.footer)

        self.setCentralWidget(central_widget)
