# Estilos modernos similares a CSS
STYLESHEET = """
    QMainWindow {
        background-color: #f5f7f9;
    }
    
    QTabWidget::pane {
        border: 1px solid #d1d8e0;
        border-radius: 6px;
        background: white;
        margin: 8px;
    }
    
    QTabBar::tab {
        background: #e9ecef;
        border: 1px solid #d1d8e0;
        border-bottom: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        padding: 8px 16px;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background: white;
        border-bottom: 2px solid #4a6cf7;
    }
    
    QScrollArea {
        border: none;
        background: transparent;
    }
    
    QFrame#sidebar {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    QCheckBox {
        spacing: 8px;
        padding: 12px;
        font-size: 14px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid #cbd5e0;
    }
    
    QCheckBox::indicator:checked {
        background-color: #4a6cf7;
        border: 1px solid #4a6cf7;
    }
    
    QCheckBox::indicator:checked:hover {
        background-color: #3b5be3;
    }
    
    QPushButton#primaryButton {
        background-color: #4a6cf7;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 12px 20px;
        font-weight: 600;
    }
    
    QPushButton#primaryButton:hover {
        background-color: #3b5be3;
    }
    
    QPushButton#primaryButton:pressed {
        background-color: #2a4bc8;
    }
    
    QFrame#contentArea {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    QLabel#title {
        font-size: 24px;
        font-weight: 600;
        color: #2d3748;
        padding: 16px;
    }
"""