from PySide6.QtWidgets import QListWidget, QListWidgetItem

class ServiceList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(200)
        self.populate()

    def populate(self):
        # TODO: Carregar serviços do ServiceManager
        services = ["CPU", "RAM", "DISK", "OS", "DEVICE", "BIOS"]
        for service in services:
            QListWidgetItem(service, self)
