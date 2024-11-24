from movimento import Movimento
from cliente import Cliente
from agencia import Agencia

class Conta:
    def __init__(self, numero, cliente, agencia, saldo_inicial=0):
        self.numero = numero
        self.cliente = cliente
        self.agencia = agencia
        self.saldo = saldo_inicial
        self.extrato = []

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            movimento = Movimento('entrada', valor)
            self.extrato.append(movimento)
            print(f"Depósito de {valor} realizado com sucesso!")
        else:
            print("Valor de depósito inválido.")

    def sacar(self, valor):
        if valor > 0 and self.saldo >= valor:
            self.saldo -= valor
            movimento = Movimento('saída', valor)
            self.extrato.append(movimento)
            print(f"Saque de {valor} realizado com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")

    def to_dict(self):
        return {
            "numero": self.numero,
            "cliente": self.cliente.to_dict(),
            "agencia": self.agencia.to_dict(),
            "saldo": self.saldo
        }

    @staticmethod
    def from_dict(data):
        try:
            # Aqui vamos lidar com a string de dados e criar um objeto Conta
            # Assumindo que a string de entrada é no formato correto
            parts = data.strip("{}").split(", ")
            numero = parts[0].split(": ")[1].strip("'")
            cliente_data = ", ".join(parts[1:4])
            agencia_data = ", ".join(parts[4:7])
            saldo = float(parts[7].split(": ")[1].strip("'"))
            cliente = Cliente.from_dict(cliente_data)
            agencia = Agencia.from_dict(agencia_data)
            return Conta(numero, cliente, agencia, saldo)
        except (ValueError, IndexError) as e:
            print(f"Erro ao converter dados da conta: {data} - {e}")
            return None

    def get_extrato(self):
        return self.extrato


class ContaCorrente(Conta):
    """Classe que representa uma Conta Corrente, com funcionalidades adicionais."""

    def __init__(self, numero, cliente, agencia, saldo_inicial=0, limite=0):
        super().__init__(numero, cliente, agencia, saldo_inicial)
        self.__limite = limite

    def depositar(self, valor):
        """Depósito na conta corrente."""
        super().depositar(valor)

    def sacar(self, valor):
        """Saque com verificação do limite de conta corrente."""
        if valor > 0 and self.saldo + self.__limite >= valor:
            self.saldo -= valor
            movimento = Movimento('saída', valor)
            self.extrato.append(movimento)
            print(f"Saque de {valor} realizado com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")

    @classmethod
    def from_dict(cls, data):
        try:
            # Aqui vai o método from_dict para ContaCorrente, semelhante ao de Conta
            parts = data.strip("{}").split(", ")
            numero = parts[0].split(": ")[1].strip("'")
            cliente_data = ", ".join(parts[1:4])
            agencia_data = ", ".join(parts[4:7])
            saldo = float(parts[7].split(": ")[1].strip("'"))
            limite = float(parts[8].split(": ")[1].strip("'"))
            cliente = Cliente.from_dict(cliente_data)
            agencia = Agencia.from_dict(agencia_data)
            return cls(numero, cliente, agencia, saldo, limite)
        except (ValueError, IndexError) as e:
            print(f"Erro ao converter dados da conta corrente: {data} - {e}")
            return None

    def get_limite(self):
        """Retorna o limite da conta corrente."""
        return self.__limite

    def set_limite(self, limite):
        """Define um novo limite para a conta corrente."""
        self.__limite = limite


class ContaEspecial(Conta):
    """Classe que representa uma Conta Especial, com limite diferenciado."""

    def __init__(self, numero, cliente, agencia, saldo_inicial=0, limite=0):
        super().__init__(numero, cliente, agencia, saldo_inicial)
        self.__limite = limite

    def to_dict(self):
        """Converte a conta especial em um dicionário, incluindo o limite."""
        conta_dict = super().to_dict()
        conta_dict["limite"] = self.__limite
        return conta_dict

    @classmethod
    def from_dict(cls, data):
        try:
            parts = data.strip("{}").split(", ")
            numero = parts[0].split(": ")[1].strip("'")
            cliente_data = ", ".join(parts[1:4])
            agencia_data = ", ".join(parts[4:7])
            saldo = float(parts[7].split(": ")[1].strip("'"))
            limite = float(parts[8].split(": ")[1].strip("'"))
            cliente = Cliente.from_dict(cliente_data)
            agencia = Agencia.from_dict(agencia_data)
            return cls(numero, cliente, agencia, saldo, limite)
        except (ValueError, IndexError) as e:
            print(f"Erro ao converter dados da conta especial: {data} - {e}")
            return None
