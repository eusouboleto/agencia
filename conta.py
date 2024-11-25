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

    def to_string(self):
        return f"tipo: Conta | numero: {self.numero} | cliente: {self.cliente.to_string()} | agencia: {self.agencia.to_string()} | saldo: {self.saldo}"

    @staticmethod
    def from_dict(data):
        try:
            numero = data.get("numero")
            cliente_data = data.get("cliente")
            agencia_data = data.get("agencia")
            saldo = data.get("saldo", 0)
            cliente = Cliente.from_dict(cliente_data)
            agencia = Agencia.from_dict(agencia_data)
            return Conta(numero, cliente, agencia, saldo)
        except (ValueError, TypeError) as e:
            print(f"Erro ao converter dados da conta: {e}")
            return None
 
    # @staticmethod
    # def from_string(data):
    #     try:
    #         # Dividindo a string de dados em partes
    #         parts = data.split(" | ")

    #         tipo = parts[0].split(":")[1].strip()  # Tipo da conta
    #         numero = parts[1].split(":")[1].strip()  # Número da conta (tratado como string)

    #         # Buscando os dados do cliente e agencia corretamente
    #         cliente_str = None
    #         agencia_str = None
    #         for part in parts:
    #             if "cliente:" in part:
    #                 cliente_str = part.split(":")[1].strip()  # Extrai a parte após "cliente:"
    #             elif "agencia:" in part:
    #                 agencia_str = part.split(":")[1].strip()  # Extrai a parte após "agencia:"

    #         if not cliente_str or not agencia_str:
    #             print(f"Erro: Dados de cliente ou agência não encontrados.")
    #             return None

    #         # Extraindo o saldo corretamente
    #         saldo_str = None
    #         for part in parts:
    #             if "saldo:" in part:
    #                 saldo_str = part.split(":")[1].strip()
    #                 break

    #         if saldo_str is None:
    #             print(f"Erro: não foi possível encontrar o saldo na string.")
    #             return None

    #         print(f"Saldo extraído: '{saldo_str}'")  # Para verificar o valor extraído

    #         try:
    #             saldo = float(saldo_str)  # Tentando converter o saldo para float
    #         except ValueError:
    #             print(f"Erro ao converter saldo para float: '{saldo_str}'")
    #             return None

    #         # Ajustando a extração correta do id_cliente e id_agencia
    #         # Agora extraímos corretamente o id do cliente e da agência
    #         cliente_data = "id_cliente:" + cliente_str  # Exemplo: "id_cliente: 2"
    #         agencia_data = "id_agencia:" + agencia_str  # Exemplo: "id_agencia: 1"

    #         cliente = Cliente.from_string(cliente_data)  # Passando os dados corretos para Cliente
    #         agencia = Agencia.from_string(agencia_data)  # Passando os dados corretos para Agencia

    #         if tipo == "ContaCorrente":
    #             return ContaCorrente(numero, cliente, agencia, saldo)
    #         elif tipo == "ContaEspecial":
    #             return ContaEspecial(numero, cliente, agencia, saldo)
    #         else:
    #             return Conta(numero, cliente, agencia, saldo)

    #     except Exception as e:
    #         print(f"Erro ao processar a string da conta: {e}")
    #         return None

    @staticmethod
    def from_string(data):
        try:
            # Dividindo a string de dados em partes
            parts = data.split(" | ")
            
            # Extraindo os dados corretamente
            tipo = parts[0].split(":")[1].strip()
            numero = parts[1].split(":")[1].strip()
            
            # Identificando os dados de cliente e agência
            cliente_str = next(part for part in parts if "cliente:" in part)
            agencia_str = next(part for part in parts if "agencia:" in part)
            
            # Convertendo para objetos
            cliente = Cliente.from_string(cliente_str)
            agencia = Agencia.from_string(agencia_str)
            
            # Extraindo o saldo
            saldo = float(next(part.split(":")[1].strip() for part in parts if "saldo:" in part))
            
            return Conta(numero, cliente, agencia, saldo)
        except Exception as e:
            print(f"Erro ao processar os dados da conta: {e}")
            return None


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

    def to_string(self):
        return f"tipo: ContaCorrente | numero: {self.numero} | cliente: {self.cliente.to_string()} | agencia: {self.agencia.to_string()} | saldo: {self.saldo} | limite: {self.__limite}"


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

    def to_string(self):
        return f"tipo: ContaEspecial | numero: {self.numero} | cliente: {self.cliente.to_string()} | agencia: {self.agencia.to_string()} | saldo: {self.saldo} | limite: {self.__limite}"
