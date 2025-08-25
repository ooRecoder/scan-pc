import wmi


class BiosService:
    """
    Serviço responsável por coletar informações da BIOS no Windows usando WMI.

    Funcionalidades principais:
    - Recupera número de série
    - Recupera versão da BIOS (SMBIOS)
    - Recupera data de release
    """
    def __init__(self):
        self.wmi_client = wmi.WMI()

    def collect(self):
        """
        Retorna um dicionário com as informações da BIOS.
        Caso haja múltiplas entradas, retorna a primeira encontrada.
        """
        
        bios_info = {}
        for bios in self.wmi_client.Win32_BIOS():
            print(bios)
            bios_info["Serial"] = bios.SerialNumber
            bios_info["Versão"] = bios.BIOSVersion
            bios_info["Release Date"] = bios.ReleaseDate
            bios_info["Status"] = bios.Status
            bios_info["Manufacturer"] = bios.Manufacturer
            
        return {"BIOS": bios_info}
