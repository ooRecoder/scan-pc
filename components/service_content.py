from PySide6.QtWidgets import (QStackedWidget, QWidget, QVBoxLayout, QLabel, 
                               QCheckBox, QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox,
                               QGroupBox, QFormLayout)
from PySide6.QtCore import Qt

from core import ServiceManager

class ServiceContentArea(QStackedWidget):
    """Área de conteúdo para configurações de serviços"""
    def __init__(self, service_manager: ServiceManager, parent=None):
        super().__init__(parent)
        self.service_manager = service_manager
        self.setObjectName("contentArea")
        
        # Página inicial (vazia)
        self.initial_page = QWidget()
        initial_layout = QVBoxLayout(self.initial_page)
        initial_layout.addWidget(QLabel("Selecione um serviço para configurar"))
        self.addWidget(self.initial_page)
        
        # Criar páginas para cada serviço
        self.service_pages = {}
        for service_name in self.service_manager.get_service_names():
            self.add_service_page(service_name)
    
    def add_service_page(self, service_name):
        """Adiciona uma página de configuração para um serviço"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título do serviço
        title = QLabel(service_name)
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Descrição do serviço
        description = self.service_manager.get_service_description(service_name)
        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #666; margin-bottom: 16px;")
            layout.addWidget(desc_label)
        
        # Opções do serviço
        options = self.service_manager.get_service_options(service_name)
        if options:
            options_group = QGroupBox("Opções de Configuração")
            options_group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #e2e8f0;
                    border-radius: 6px;
                    margin-top: 16px;
                    padding-top: 12px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 8px;
                    padding: 0 5px 0 5px;
                }
            """)
            
            form_layout = QFormLayout()
            form_layout.setVerticalSpacing(12)
            form_layout.setHorizontalSpacing(20)
            
            for option_name, option_data in options.items():
                option_widget = self.create_option_widget(option_data)
                if option_widget:
                    # Adicionar tooltip com a descrição
                    description = option_data.get('description', '')
                    if description:
                        option_widget.setToolTip(description)
                    
                    form_layout.addRow(QLabel(option_name + ":"), option_widget)
            
            options_group.setLayout(form_layout)
            layout.addWidget(options_group)
        else:
            no_options_label = QLabel("Este serviço não possui opções de configuração.")
            no_options_label.setStyleSheet("color: #888; font-style: italic;")
            layout.addWidget(no_options_label)
        
        layout.addStretch()
        self.addWidget(page)
        self.service_pages[service_name] = page
    
    def create_option_widget(self, option_data):
        """Cria o widget apropriado para o tipo de opção"""
        option_type = option_data.get('type', '')
        default_value = option_data.get('default')
        
        if option_type == 'boolean':
            checkbox = QCheckBox()
            checkbox.setChecked(bool(default_value))
            return checkbox
        
        elif option_type == 'string':
            # Verificar se há opções pré-definidas
            if 'options' in option_data:
                combobox = QComboBox()
                combobox.addItems(option_data['options'])
                if default_value in option_data['options']:
                    combobox.setCurrentText(default_value)
                return combobox
            else:
                line_edit = QLineEdit(str(default_value))
                return line_edit
        
        elif option_type == 'integer':
            spinbox = QSpinBox()
            spinbox.setRange(0, 999999)
            spinbox.setValue(int(default_value))
            return spinbox
        
        elif option_type == 'float' or option_type == 'double':
            spinbox = QDoubleSpinBox()
            spinbox.setRange(0, 999999.99)
            spinbox.setValue(float(default_value))
            return spinbox
        
        # Tipo desconhecido ou não suportado
        return QLabel(str(default_value))
    
    def show_service(self, service_name):
        """Exibe a página de configuração de um serviço específico"""
        if service_name in self.service_pages:
            self.setCurrentWidget(self.service_pages[service_name])
        else:
            self.setCurrentWidget(self.initial_page)