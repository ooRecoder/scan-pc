import tkinter as tk
from tkinter import ttk
from core.config_manager import ConfigManager
from core.services import ServiceManager
from core.machines import ComputerManager

class VerificationTab(ttk.Frame):
    def __init__(self, parent, sm: ServiceManager, cmgr: ComputerManager):
        super().__init__(parent)
        self.sm = sm
        self.cmgr = cmgr

        self.selected_computer = tk.StringVar()
        self.service_vars = {}      # Checkbox de serviços
        self.field_vars = {}        # Checkbox de campos por serviço

        self.build_ui()

    def build_ui(self):
        # Canvas + scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Dropdown de computadores
        ttk.Label(self.scrollable_frame, text="Selecionar computador:").pack(anchor="w", padx=5, pady=2)
        computers = self.cmgr.list_computers()
        self.comp_cb = ttk.Combobox(self.scrollable_frame, textvariable=self.selected_computer, values=computers, state="readonly")
        self.comp_cb.pack(anchor="w", padx=5, pady=2)
        self.comp_cb.bind("<<ComboboxSelected>>", lambda e: self.show_services())

        # Frames para checkboxes
        self.services_frame = ttk.LabelFrame(self.scrollable_frame, text="Serviços")
        self.services_frame.pack(fill="x", padx=5, pady=5)
        self.fields_frame = ttk.LabelFrame(self.scrollable_frame, text="Campos do serviço selecionado")
        self.fields_frame.pack(fill="x", padx=5, pady=5)

        # Botão para exibir resultado
        self.show_btn = ttk.Button(self.scrollable_frame, text="Exibir informações selecionadas", command=self.show_selected_info)
        self.show_btn.pack(pady=5)

        # Text para mostrar resultado
        self.result_text = tk.Text(self.scrollable_frame, height=20)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def show_services(self):
        # Limpa checkboxes anteriores
        for widget in self.services_frame.winfo_children():
            widget.destroy()
        self.service_vars.clear()

        comp_id = self.selected_computer.get()
        computer = self.cmgr.get_computer(comp_id)
        if not computer:
            return

        # Cria checkboxes para cada serviço presente nesse computador
        for svc in computer.keys():
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(self.services_frame, text=svc, variable=var, command=self.show_fields)
            chk.pack(anchor="w", padx=5, pady=2)
            self.service_vars[svc] = var

        self.show_fields()

    def show_fields(self):
        # Limpa checkboxes anteriores
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        self.field_vars.clear()

        comp_id = self.selected_computer.get()
        computer = self.cmgr.get_computer(comp_id)
        if not computer:
            return

        # Para cada serviço selecionado, mostra campos
        for svc, svc_var in self.service_vars.items():
            if not svc_var.get():
                continue
            frame = ttk.LabelFrame(self.fields_frame, text=svc)
            frame.pack(fill="x", padx=5, pady=2)
            for key in computer[svc].keys():
                var = tk.BooleanVar(value=True)
                chk = ttk.Checkbutton(frame, text=key, variable=var)
                chk.pack(anchor="w", padx=5, pady=1)
                self.field_vars[f"{svc}:{key}"] = var

    def show_selected_info(self):
        self.result_text.delete("1.0", tk.END)
        comp_id = self.selected_computer.get()
        computer = self.cmgr.get_computer(comp_id)
        if not computer:
            self.result_text.insert(tk.END, "Nenhum computador selecionado.\n")
            return

        result = {}
        for svc, svc_var in self.service_vars.items():
            if not svc_var.get() or svc not in computer:
                continue
            result[svc] = {}
            for key, key_var in self.field_vars.items():
                s, k = key.split(":", 1)
                if s == svc and key_var.get():
                    result[svc][k] = computer[svc][k]

        import json
        self.result_text.insert(tk.END, json.dumps(result, indent=4, ensure_ascii=False))
