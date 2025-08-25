import tkinter as tk
from tkinter import ttk
from gui.tooltip import Tooltip

class ServiceFrame(ttk.Frame):
    def __init__(self, parent, service_name, service_manager, config_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.service_name = service_name
        self.sm = service_manager
        self.cm = config_manager
        self.option_vars = {}
        self.build_frame()

    def build_frame(self):
        options = self.sm.get_service_options(self.service_name)
        config = self.cm.get_service_config(self.service_name)

        if not options:
            ttk.Label(self, text="Sem opções disponíveis").pack()
            return

        for opt_name, opt_data in options.items():
            default_val = config.get(opt_name, opt_data.get("default"))

            # Para boolean
            if opt_data["type"] == "boolean":
                var = tk.BooleanVar(value=default_val)
                chk = ttk.Checkbutton(
                    self,
                    text=opt_name,
                    variable=var,
                    command=lambda n=opt_name, v=var: self.update_config(n, v.get())
                )
                chk.pack(anchor="w", padx=5, pady=2)
                self.option_vars[opt_name] = var

                # Tooltip com descrição
                desc = self.sm.get_option_description(self.service_name, opt_name)
                Tooltip(chk, desc)

            # Para string / dropdown
            elif opt_data["type"] == "string":
                var = tk.StringVar(value=default_val)
                choices = opt_data.get("options", [])
                lbl = ttk.Label(self, text=opt_name)
                lbl.pack(anchor="w", padx=5)
                cb = ttk.Combobox(self, textvariable=var, values=choices, state="readonly")
                cb.pack(anchor="w", padx=15, pady=2)
                cb.bind("<<ComboboxSelected>>", lambda e, n=opt_name, v=var: self.update_config(n, v.get()))
                self.option_vars[opt_name] = var

                # Tooltip para a label
                desc = self.sm.get_option_description(self.service_name, opt_name)
                Tooltip(lbl, desc)

    def update_config(self, option_name, value):
        config = self.cm.get_service_config(self.service_name)
        config[option_name] = value
        self.cm.set_service_config(self.service_name, config)
