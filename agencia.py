class Agencia:
    def __init__(self, id_agencia, nome, endereco, cnpj=None, telefone=None):
        self.id_agencia = id_agencia
        self.nome = nome
        self.endereco = endereco
        self.cnpj = cnpj
        self.telefone = telefone

    def to_dict(self):
        return {
            "id_agencia": self.id_agencia,
            "nome": self.nome,
            "endereco": self.endereco,
            "cnpj": self.cnpj,
            "telefone": self.telefone
        }

    def to_string(self):
        return f"id_agencia: {self.id_agencia} | nome: {self.nome} | endereco: {self.endereco} | cnpj: {self.cnpj} | telefone: {self.telefone}"

    @staticmethod
    def from_dict(data):
        # Verifica se os dados estão em formato de dicionário
        if isinstance(data, dict):
            return Agencia(
                data.get("id_agencia", ""),
                data.get("nome", ""),
                data.get("endereco", ""),
                data.get("cnpj", None),
                data.get("telefone", None)
            )
        
        # Caso os dados sejam uma string com formato específico
        try:
            if " | " in data:
                dados = data.split(" | ")
                if len(dados) != 5:  # A agência tem 5 campos
                    print("Formato inválido, dados incompletos:", data)
                    return None

                id_agencia = dados[0].split(":")[1].strip()
                nome = dados[1].split(":")[1].strip()
                endereco = dados[2].split(":")[1].strip()
                cnpj = dados[3].split(":")[1].strip()
                telefone = dados[4].split(":")[1].strip()

                return Agencia(id_agencia, nome, endereco, cnpj, telefone)
            else:
                print("Formato inválido para dados de agência:", data)
                return None
        except Exception as e:
            print(f"Erro ao processar dados de agência: {e}")
            return None

    @staticmethod
    def from_string(data):
        # Método para reconstruir uma agência a partir de uma string (para carregar do .txt)
        return Agencia.from_dict(data)
