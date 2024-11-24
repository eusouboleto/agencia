import os
from cliente import Cliente
from agencia import Agencia
from conta import ContaCorrente
from movimento import Movimento

# Função para carregar dados de arquivos, usando tipo_item para determinar a classe a ser instanciada
def carregar_dados(nome_arquivo, tipo_item):
    lista = []
    if os.path.exists(nome_arquivo):  # Verifica se o arquivo existe
        with open(nome_arquivo, "r") as arquivo:
            dados = arquivo.readlines()
            for linha in dados:
                linha = linha.strip()  # Remove quebras de linha e espaços extras
                partes = linha.split(" | ")
                try:
                    # Verifica o tipo de item e chama o método estático apropriado para reconstrução
                    if tipo_item == Cliente:
                        item = Cliente.from_string(linha)
                    elif tipo_item == Agencia:
                        item = Agencia.from_string(linha)
                    elif tipo_item == ContaCorrente:
                        item = ContaCorrente.from_string(linha)
                    elif tipo_item == Movimento:
                        item = Movimento.from_string(linha)
                    else:
                        print(f"Tipo desconhecido: {tipo_item}")
                        continue
                    
                    lista.append(item)
                except Exception as e:
                    print(f"Erro ao carregar a linha: '{linha}'. Erro: {e}")
    return lista

# Função para salvar dados em arquivos, verificando o tipo do objeto e formatando adequadamente
def salvar_dados(nome_arquivo, dados, sobrescrever=False):
    modo = "w" if sobrescrever else "a"  # Usando "w" para sobrescrever ou "a" para adicionar
    try:
        with open(nome_arquivo, modo) as arquivo:
            for dado in dados:
                if isinstance(dado, Cliente):
                    arquivo.write(dado.to_string() + "\n")
                elif isinstance(dado, Agencia):
                    arquivo.write(dado.to_string() + "\n")
                elif isinstance(dado, ContaCorrente):
                    arquivo.write(dado.to_string() + "\n")
                elif isinstance(dado, Movimento):
                    arquivo.write(dado.to_string() + "\n")
                else:
                    print(f"Tipo desconhecido: {type(dado)}")
    except Exception as e:
        print(f"Erro ao abrir ou escrever no arquivo {nome_arquivo}: {e}")