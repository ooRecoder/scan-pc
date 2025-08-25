import tkinter as tk
from tkinter import ttk, messagebox
from core import ServiceManager, ConfigManager, ComputerManager, Scanner
from gui.service_frame import ServiceFrame
from .verification_tab import VerificationTab
from gui.tooltip import Tooltip


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuração de Serviços")
        self.geometry("900x600")

        self.sm = ServiceManager()
        self.cm = ConfigManager()
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Aba de configuração
        self.config_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.config_tab, text="Configuração")

        # Aba de verificação
        self.verif_tab = VerificationTab(self.notebook, self.sm, ComputerManager())
        self.notebook.add(self.verif_tab, text="Verificação")

        self.build_ui()

    def build_ui(self):
        # Painel esquerdo e direito dentro da aba de configuração
        self.left_frame = ttk.Frame(self.config_tab)
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.right_frame = ttk.Frame(self.config_tab)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.service_vars = {}
        for svc in self.sm.get_service_names():
            var = tk.BooleanVar(value=svc in self.cm.config)
            chk = ttk.Checkbutton(
                self.left_frame,
                text=svc,
                variable=var,
                command=lambda s=svc, v=var: self.toggle_service(s, v.get())
            )
            chk.pack(anchor="w", pady=2)
            self.service_vars[svc] = var

            # Adiciona tooltip usando get_service_description
            desc = self.sm.get_service_description(svc) or "Sem descrição disponível"
            Tooltip(chk, desc)

        # Botão para executar serviços
        btn_run = ttk.Button(self.left_frame, text="Executar Serviços", command=self.run_services)
        btn_run.pack(pady=10)

        # Frame atual do serviço selecionado
        self.current_frame = None
        # Mostra opções dos serviços já habilitados na configuração
        for svc, var in self.service_vars.items():
            if var.get():
                self.show_service_options(svc)
                break  # mostra apenas o primeiro serviço habilitado

    def toggle_service(self, service_name, enabled):
        if enabled:
            # Adiciona serviço no config se não existir, com defaults
            options = {}
            service_options = self.sm.get_service_options(service_name)
            if service_options:
                for k, v in service_options.items():
                    options[k] = v.get("default")
            self.cm.set_service_config(service_name, options)
            self.show_service_options(service_name)
        else:
            self.cm.remove_service(service_name)
            self.clear_service_frame()

    def clear_service_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_service_options(self, service_name):
        self.clear_service_frame()
        self.current_frame = ServiceFrame(self.right_frame, service_name, self.sm, self.cm)
        self.current_frame.pack(fill="both", expand=True)

    def run_services(self):
        scanner = Scanner()
        results = scanner.run(save=True)
        messagebox.showinfo("Execução concluída", f"Serviços executados. Resultados salvos.")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
