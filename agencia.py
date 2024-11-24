class Agencia:
    codigo_sequencial = 1

    def __init__(self, nome, endereco):
        self.codigo = Agencia.codigo_sequencial
        Agencia.codigo_sequencial += 1
        self.nome = nome
        self.endereco = endereco

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "endereco": self.endereco
        }

    @staticmethod
    def from_dict(data):
        # Se data é um dicionário, reconstrói a instância usando os valores do dicionário
        if isinstance(data, dict):
            nome = data.get("nome", "")
            endereco = data.get("endereco", "")
            codigo = int(data.get("codigo", Agencia.codigo_sequencial))
            
            # Atualiza `codigo_sequencial` para evitar conflito
            if codigo >= Agencia.codigo_sequencial:
                Agencia.codigo_sequencial = codigo + 1
            
            # Retorna uma nova instância de Agencia com o código definido
            agencia = Agencia(nome, endereco)
            agencia.codigo = codigo
            return agencia
        
        # Se `data` for uma string no formato esperado
        try:
            # Corrige o processo de separação para garantir que os dados sejam lidos corretamente
            partes = data.split(" | ")
            if len(partes) != 3:
                raise ValueError("Formato inválido")
            
            codigo = partes[0].split(":")[1].strip()
            nome = partes[1].split(":")[1].strip()
            endereco = partes[2].split(":")[1].strip()
            
            # Cria uma nova instância de Agencia
            agencia = Agencia(nome, endereco)
            agencia.codigo = int(codigo)
            
            # Atualiza o código sequencial
            if agencia.codigo >= Agencia.codigo_sequencial:
                Agencia.codigo_sequencial = agencia.codigo + 1

            return agencia
        
        except Exception as e:
            print(f"Erro ao processar dados de agência: {e}")
            return None