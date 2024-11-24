import os

# Função para carregar os dados dos arquivos
def carregar_dados(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []  # Retorna uma lista vazia se o arquivo não existir
    with open(nome_arquivo, "r") as arquivo:
        dados = arquivo.readlines()
        return [linha.strip() for linha in dados]  # Remove quebras de linha

def salvar_dados(nome_arquivo, dados):
    with open(nome_arquivo, "w") as arquivo:  # Sobrescreve o arquivo a cada vez
        for dado in dados:
            if "id_cliente" in dado:
                # Salva dados de Cliente
                arquivo.write(f"ID_Cliente: {dado['id_cliente']} |  Nome_Cliente: {dado['nome']} | CPF: {dado['cpf']}\n")
            elif "codigo" in dado:
                # Salva dados de Agencia
                arquivo.write(f"ID_Agência: {dado['codigo']} | Nome_Agência: {dado['nome']} | Endereço:{dado['endereco']}\n")
            elif "numero_conta" in dado:
                # Salva dados de Conta
                arquivo.write(f"Nº da Conta: {dado['numero_conta']} | ID_Cliente: {dado['cliente_id']} | ID_Agência: {dado['agencia_id']} | Saldo da conta: {dado['saldo']}\n")