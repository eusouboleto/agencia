from datetime import datetime

class Movimento:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
        self.data = datetime.now()

    def to_dict(self):
        return f"{self.tipo}, {self.valor}, {self.data.isoformat()}"

    @staticmethod
    def from_dict(data):
        tipo, valor, data_str = data.split(", ")
        return Movimento(tipo, float(valor))
