import json
from typing import Dict, Any, Optional, Union, List

class ServiceManager:
    def __init__(self, json_file_path: str = "json/services.json"):
        """
        Inicializa o gerenciador de serviços com o caminho do arquivo JSON
        
        Args:
            json_file_path (str): Caminho para o arquivo JSON de configuração
        """
        self.json_file_path = json_file_path
        self.services_data: Dict[str, Dict[str, Any]] = self._load_services()
    
    def _load_services(self) -> Dict[str, Dict[str, Any]]:
        """
        Carrega os dados dos serviços do arquivo JSON
        
        Returns:
            Dict[str, Dict[str, Any]]: Dicionário com os dados dos serviços
            
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            json.JSONDecodeError: Se o JSON estiver mal formatado
        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo JSON não encontrado: {self.json_file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Erro ao decodificar JSON: {e}", e.doc, e.pos)
    
    def save_services(self) -> None:
        """
        Salva os dados dos serviços de volta para o arquivo JSON
        
        Raises:
            IOError: Se ocorrer erro ao salvar o arquivo
        """
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.services_data, file, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Erro ao salvar arquivo JSON: {e}")
    
    def get_all_services(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna todos os serviços disponíveis
        
        Returns:
            Dict[str, Dict[str, Any]]: Dicionário com todos os serviços
        """
        return self.services_data
    
    def get_service(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtém um serviço específico pelo nome
        
        Args:
            service_name (str): Nome do serviço (ex: "CPU", "DEVICE")
            
        Returns:
            Optional[Dict[str, Any]]: Dados do serviço ou None se não existir
        """
        return self.services_data.get(service_name.upper())
    
    def service_exists(self, service_name: str) -> bool:
        """
        Verifica se um serviço existe
        
        Args:
            service_name (str): Nome do serviço
            
        Returns:
            bool: True se o serviço existe, False caso contrário
        """
        return service_name.upper() in self.services_data
    
    def get_service_description(self, service_name: str) -> Optional[str]:
        """
        Obtém a descrição de um serviço
        
        Args:
            service_name (str): Nome do serviço
            
        Returns:
            Optional[str]: Descrição do serviço ou None se não existir
        """
        service = self.get_service(service_name)
        return service.get('description') if service else None
    
    def get_service_options(self, service_name: str) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Obtém as opções de um serviço
        
        Args:
            service_name (str): Nome do serviço
            
        Returns:
            Optional[Dict[str, Dict[str, Any]]]: Opções do serviço ou None se não existir
        """
        service = self.get_service(service_name)
        return service.get('options') if service else None
    
    def get_option_value(self, service_name: str, option_name: str) -> Optional[Any]:
        """
        Obtém o valor de uma opção específica de um serviço
        
        Args:
            service_name (str): Nome do serviço
            option_name (str): Nome da opção
            
        Returns:
            Optional[Any]: Valor da opção ou None se não existir
        """
        options = self.get_service_options(service_name)
        if options and option_name in options:
            return options[option_name].get('default')
        return None
    
    def get_enabled_options(self, service_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Obtém todas as opções habilitadas de um serviço
        
        Args:
            service_name (str): Nome do serviço
            
        Returns:
            Dict[str, Dict[str, Any]]: Dicionário com as opções habilitadas
        """
        options = self.get_service_options(service_name)
        if not options:
            return {}
        
        enabled_options = {}
        for option_name, option_data in options.items():
            if option_data.get('default', False):
                enabled_options[option_name] = option_data
        
        return enabled_options
    
    def add_service(self, service_name: str, description: str, options: Optional[Dict[str, Dict[str, Any]]] = None) -> bool:
        """
        Adiciona um novo serviço
        
        Args:
            service_name (str): Nome do serviço
            description (str): Descrição do serviço
            options (Optional[Dict[str, Dict[str, Any]]]): Opções do serviço
            
        Returns:
            bool: True se o serviço foi adicionado, False se já existe
        """
        if self.service_exists(service_name):
            return False
        
        service_data: Dict[str, Any] = {
            'description': description
        }
        
        if options:
            service_data['options'] = options
        
        self.services_data[service_name.upper()] = service_data
        return True
    
    def remove_service(self, service_name: str) -> bool:
        """
        Remove um serviço
        
        Args:
            service_name (str): Nome do serviço
            
        Returns:
            bool: True se o serviço foi removido, False se não existe
        """
        if service_name.upper() in self.services_data:
            del self.services_data[service_name.upper()]
            return True
        return False
    
    def validate_configuration(self) -> bool:
        """
        Valida a configuração completa dos serviços
        
        Returns:
            bool: True se a configuração é válida, False caso contrário
        """
        try:
            for service_name, service_data in self.services_data.items():
                if 'description' not in service_data:
                    return False
                
                if 'options' in service_data:
                    for option_name, option_data in service_data['options'].items():
                        if 'type' not in option_data or 'default' not in option_data or 'description' not in option_data:
                            return False
            
            return True
        except (AttributeError, TypeError):
            return False

    def get_service_names(self) -> List[str]:
        """
        Retorna uma lista com os nomes de todos os serviços
        
        Returns:
            List[str]: Lista de nomes de serviços
        """
        return list(self.services_data.keys())
    
    def get_option_info(self, service_name: str, option_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações completas de uma opção específica
        
        Args:
            service_name (str): Nome do serviço
            option_name (str): Nome da opção
            
        Returns:
            Optional[Dict[str, Any]]: Informações da opção ou None se não existir
        """
        options = self.get_service_options(service_name)
        return options.get(option_name) if options else None
    
    def get_option_choices(self, service_name: str, option_name: str) -> Optional[List[Any]]:
        options = self.get_service_options(service_name)
        if options and option_name in options:
            return options[option_name].get("options")
        return None

    def get_option_description(self, service_name: str, option_name: str) -> Optional[str]:
        options = self.get_service_options(service_name)
        if options and option_name in options:
            return options[option_name].get("description")
        return None
