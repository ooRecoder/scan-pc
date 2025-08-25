from .base_service import BaseService
import wmi

class DeviceService(BaseService):
    """
    Serviço responsável por coletar e organizar informações detalhadas
    do sistema Windows por meio do WMI (Windows Management Instrumentation).

    Funcionalidades principais:
    - Identifica o tipo do equipamento (desktop, notebook, servidor, etc.)
    - Obtém fabricante, modelo e usuário logado
    - Recupera informações de BIOS (número de série, versão, data de release)
    - Verifica a presença e status de baterias (para diferenciar notebooks de desktops)

    Esse serviço é útil para inventário de máquinas, diagnósticos
    ou aplicações que precisem diferenciar entre notebooks e desktops.
    """

    PC_SYSTEM_TYPE_MAP = {
        0: "Unknown",
        1: "Desktop",
        2: "Laptop",
        3: "Server",
        4: "Tablet",
        5: "Convertible Notebook",
        6: "Workstation",
        7: "Enterprise Server",
        8: "Blade Server",
        9: "Mini PC / Small Form Factor",
        10: "Embedded / Appliance"
    }

    def __init__(self, **options):
        super().__init__(**options)
        # Configurações padrão
        self.options.setdefault("include_battery", True)  # incluir informações de bateria
        self.options.setdefault("include_bios", True)     # incluir informações de BIOS
        self.options.setdefault("include_system", True)  # incluir informações do sistema
        self.wmi_client = wmi.WMI()

    def collect(self):
        """
        Retorna um dicionário com informações detalhadas do sistema
        de acordo com as opções configuradas em self.options.
        """
        result = {}

        if self.options["include_system"]:
            info = {}
            for system in self.wmi_client.Win32_ComputerSystem():
                info["DeviceName"] = system.Name
                info["PC_Type"] = self.PC_SYSTEM_TYPE_MAP.get(system.PCSystemType, "Unknown")
                info["Manufacturer"] = system.Manufacturer
                info["Model"] = system.Model
                info["User"] = system.UserName
                info["Status"] = system.Status
                info["Architecture"] = system.SystemType
            result["Device"] = info

        if self.options["include_battery"]:
            battery_list = []
            for battery in self.wmi_client.Win32_Battery():
                battery_list.append({
                    "Name": battery.Name,
                    "Status": battery.BatteryStatus
                })
            result["Battery"] = battery_list

        return result
