# services/system_info_service.py

import wmi

class DeviceInfoService:
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
        2: "Notebook/Laptop",
        3: "Server",
        4: "Tablet",
        5: "Notebook Convertible",
        6: "Workstation",
        7: "Enterprise Server",
        8: "Blade Server",
        9: "Mini PC / Small Form Factor",
        10: "Embedded / Appliance"
    }

    def __init__(self, **options):
        super().__init__(**options)
        self.wmi_client = wmi.WMI()

    def collect(self):
        """
        Retorna um dicionário com informações detalhadas do sistema.
        Inclui fabricante, modelo, nome do computador, BIOS e bateria (se houver).
        """
        info = {}
        for system in self.wmi_client.Win32_ComputerSystem():
            # print(system)
            info["Nome do Dispositivo"] = system.Name
            info["PC_Type"] = self.PC_SYSTEM_TYPE_MAP.get(system.PCSystemType, "Unknown")
            info["Fabricante"] = system.Manufacturer
            info["Modelo"] = system.Model
            info["Usuário"] = system.UserName
            info["Status"] = system.Status

        # Informações de bateria (se houver)
        battery_list = []
        for battery in self.wmi_client.Win32_Battery():
            battery_list.append({
                "name": battery.Name,
                "status": battery.BatteryStatus
            })
        info["battery"] = battery_list

        return {"Device": info}
