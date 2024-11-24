class Cliente:
    def __init__(self, id_cliente, nome, cpf):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "cpf": self.cpf
        }

    @staticmethod
    def from_dict(data):
        # Se os dados estiverem em formato de dicionário
        if isinstance(data, dict):
            return Cliente(data.get("id_cliente", ""), data.get("nome", ""), data.get("cpf", ""))
        
        # Se `data` for uma string, tenta dividi-la no formato esperado
        try:
            # Verifica se a string está no formato correto (ID_Cliente: x | Nome_Cliente: y | CPF: z)
            if " | " in data:
                dados = data.split(" | ")  # Divide a string em partes
                if len(dados) != 3:
                    print("Formato inválido, dados incompletos:", data)
                    return None  # Retorna None se a string não tiver 3 partes

                id_cliente = dados[0].split(":")[1].strip()
                nome = dados[1].split(":")[1].strip()
                cpf = dados[2].split(":")[1].strip()

                return Cliente(id_cliente, nome, cpf)
            else:
                print("Formato inválido para dados de cliente:", data)
                return None
        
        except IndexError:
            print("Erro no formato da string, campos ausentes:", data)
            return None
        except ValueError as e:
            print(f"Valor inválido nos dados: {data}. Erro: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao processar dados de cliente: {e}")
            return None