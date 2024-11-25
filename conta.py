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
        # Converte a conta em um dicionário, incluindo cliente e agência
        return {
            "numero": self.numero,
            "cliente": self.cliente.to_dict(),
            "agencia": self.agencia.to_dict(),
            "saldo": self.saldo
        }

    def to_string(self):
        # Converte a conta para string para salvar no .txt
        return f"numero: {self.numero} | cliente: {self.cliente.to_string()} | agencia: {self.agencia.to_string()} | saldo: {self.saldo}"

    @staticmethod
    def from_dict(data):
        try:
            # Extrair informações do dicionário
            numero = data.get("numero")
            cliente_data = data.get("cliente")
            agencia_data = data.get("agencia")
            saldo = data.get("saldo", 0)

            # Recriar o objeto Conta a partir dos dados
            cliente = Cliente.from_dict(cliente_data)
            agencia = Agencia.from_dict(agencia_data)
            return Conta(numero, cliente, agencia, saldo)
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter dados da conta: {e}")
            return None

    @staticmethod
    def from_string(data):
        # Método para reconstruir uma conta a partir de uma string
        # Exemplo de string: "numero: 123 | cliente: ... | agencia: ... | saldo: 1000"
        try:
            parts = data.split(" | ")
            numero = int(parts[0].split(":")[1].strip())
            cliente_str = parts[1].split(":")[1].strip()
            agencia_str = parts[2].split(":")[1].strip()
            saldo = float(parts[3].split(":")[1].strip())

            cliente = Cliente.from_string(cliente_str)
            agencia = Agencia.from_string(agencia_str)
            return Conta(numero, cliente, agencia, saldo)
        except Exception as e:
            print(f"Erro ao processar a string da conta: {e}")
            return None

    def get_extrato(self):
        return self.extrato

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, agencia, saldo_inicial=0, limite=0):
        super().__init__(numero, cliente, agencia, saldo_inicial)
        self.__limite = limite

    def depositar(self, valor):
        super().depositar(valor)

    def sacar(self, valor):
        if valor > 0 and self.saldo + self.__limite >= valor:
            self.saldo -= valor
            movimento = Movimento('saída', valor)
            self.extrato.append(movimento)
            print(f"Saque de {valor} realizado com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")

    def to_dict(self):
        conta_dict = super().to_dict()
        conta_dict["limite"] = self.__limite
        return conta_dict

    @classmethod
    def from_dict(cls, data):
        conta = super().from_dict(data)
        limite = data.get("limite", 0)
        conta.__limite = limite
        return conta

    def get_limite(self):
        return self.__limite

    def set_limite(self, limite):
        self.__limite = limite

class ContaEspecial(Conta):
    def __init__(self, numero, cliente, agencia, saldo_inicial=0, limite=0):
        super().__init__(numero, cliente, agencia, saldo_inicial)
        self.__limite = limite

    def to_dict(self):
        conta_dict = super().to_dict()
        conta_dict["limite"] = self.__limite
        return conta_dict

    @classmethod
    def from_dict(cls, data):
        conta = super().from_dict(data)
        limite = data.get("limite", 0)
        conta.__limite = limite
        return conta