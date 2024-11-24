class Cliente:
    def __init__(self, id_cliente, nome, cpf, telefone=None, endereco=None, data_nascimento=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.data_nascimento = data_nascimento

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "data_nascimento": self.data_nascimento
        }

    def to_string(self):
        # Método para converter o cliente em string no formato adequado para salvar no .txt
        return f"id_cliente: {self.id_cliente} | nome: {self.nome} | cpf: {self.cpf} | telefone: {self.telefone} | endereco: {self.endereco} | data_nascimento: {self.data_nascimento}"

    @staticmethod
    def from_dict(data):
        # Verifica se os dados estão em formato de dicionário
        if isinstance(data, dict):
            return Cliente(
                data.get("id_cliente", ""),
                data.get("nome", ""),
                data.get("cpf", ""),
                data.get("telefone", None),
                data.get("endereco", None),
                data.get("data_nascimento", None)
            )
        
        # Caso os dados sejam uma string com formato específico
        try:
            if " | " in data:
                dados = data.split(" | ")
                if len(dados) != 6:
                    print("Formato inválido, dados incompletos:", data)
                    return None

                id_cliente = dados[0].split(":")[1].strip()
                nome = dados[1].split(":")[1].strip()
                cpf = dados[2].split(":")[1].strip()
                telefone = dados[3].split(":")[1].strip()
                endereco = dados[4].split(":")[1].strip()
                data_nascimento = dados[5].split(":")[1].strip()

                return Cliente(id_cliente, nome, cpf, telefone, endereco, data_nascimento)
            else:
                print("Formato inválido para dados de cliente:", data)
                return None
        except Exception as e:
            print(f"Erro ao processar dados de cliente: {e}")
            return None

    @staticmethod
    def from_string(data):
        # Método para reconstruir um cliente a partir de uma string (para carregar do .txt)
        return Cliente.from_dict(data)