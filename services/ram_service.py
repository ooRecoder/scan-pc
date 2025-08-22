import psutil
from .base_service import BaseService

class RAMService(BaseService):
    def __init__(self, **options):
        super().__init__(**options)
        # Unidade de memória: GB por padrão
        self.unit = self.options.get("unit", "GB")
        # Tipo de memória a coletar: total, disponível, usada ou porcentagem
        self.metric = self.options.get("metric", "total")  

    def collect(self) -> dict:
        mem = psutil.virtual_memory()

        value = None
        if self.metric == "total":
            value = mem.total
        elif self.metric == "available":
            value = mem.available
        elif self.metric == "used":
            value = mem.used
        elif self.metric == "percent":
            value = mem.percent
        else:
            raise ValueError(f"Métrica desconhecida: {self.metric}")

        if self.metric != "percent":  # converte unidades apenas se não for porcentagem
            if self.unit == "MB":
                value = round(value / (1024**2), 2)
            elif self.unit == "GB":
                value = round(value / (1024**3), 2)
            elif self.unit == "TB":
                value = round(value / (1024**4), 2)

        return {f"RAM_{self.metric}": f"{value} {self.unit if self.metric != 'percent' else '%'}"}
