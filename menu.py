from cliente import Cliente
from agencia import Agencia
from conta import ContaCorrente
from persistencia import salvar_dados, carregar_dados
from movimento import Movimento
import re

# Listas para armazenar clientes, agências, contas e movimentações
clientes = []
agencias = []
contas = []

# Função para validar o CPF
def validar_cpf(cpf):
    if re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
        return True
    return False

# Função para validar o ID de cliente e agência
def validar_cliente_agencia(cliente_id, agencia_id):
    cliente = next((cl for cl in clientes if cl.id_cliente == cliente_id), None)
    agencia = next((ag for ag in agencias if ag.codigo == agencia_id), None)
    return cliente, agencia

# Função para exibir o menu principal
def menu_principal():
    while True:
        print("\nMenu Principal do Sistema Bancário")
        print("1. Menu de Clientes")
        print("2. Menu de Agências")
        print("3. Menu de Contas")
        print("4. Menu de Movimentações")
        print("5. Sair do Programa")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_agencias()
        elif opcao == "3":
            menu_contas()
        elif opcao == "4":
            menu_movimentos()
        elif opcao == "5":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Função genérica para cadastrar qualquer item
def cadastrar_item(nome_item, tipo_item, lista_items, arquivo):
    nome = input(f"Nome do {nome_item}: ")
    id_item = str(len(lista_items) + 1)
    
    if nome_item == "Cliente":
        while not validar_cpf(nome):
            print("CPF inválido! Tente novamente.")
            nome = input(f"Nome do {nome_item}: ")
    
    # Verifica se o cliente já existe na lista (com base no CPF ou ID)
    if nome_item == "Cliente":
        if any(cliente.cpf == nome for cliente in lista_items):  # Evita CPF duplicado
            print(f"Cliente com CPF {nome} já cadastrado!")
            return None  # Retorna None se já existir
    
    item = tipo_item(id_item, nome)
    lista_items.append(item)

    # Reescreve todos os dados no arquivo
    salvar_dados(arquivo, [item.to_dict() for item in lista_items])
    print(f"{nome_item} {nome} cadastrado com sucesso!")
    return item

# Menu de Clientes (Inserção, Alteração, Consulta, Remoção)
def menu_clientes():
    while True:
        print("\nMenu de Clientes")
        print("1. Inserção de Cliente")
        print("2. Alteração de Cliente")
        print("3. Consulta de Clientes")
        print("4. Remoção de Cliente")
        print("5. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_inserir_cliente()
        elif opcao == "2":
            menu_alterar_cliente()
        elif opcao == "3":
            menu_consultar_clientes()
        elif opcao == "4":
            menu_remover_cliente()
        elif opcao == "5":
            break
        else:
            print("Opção inválida! Tente novamente.")

# Inserção de Cliente
def menu_inserir_cliente():
    print("\nInserção de Cliente")
    nome = input("Nome do cliente: ")
    cpf = input("CPF do cliente (formato: xxx.xxx.xxx-xx): ")
    
    if not validar_cpf(cpf):
        print("CPF inválido! Tente novamente.")
        return
    
    cliente = Cliente(str(len(clientes) + 1), nome, cpf)
    clientes.append(cliente)
    salvar_dados("clientes.txt", [cliente.to_dict() for cliente in clientes])
    print(f"Cliente {nome} cadastrado com sucesso!")

# Alteração de Cliente
def menu_alterar_cliente():
    cliente_id = input("ID do Cliente a ser alterado: ")
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    
    if cliente:
        novo_nome = input(f"Novo nome para o cliente {cliente.nome}: ")
        novo_cpf = input(f"Novo CPF para o cliente {cliente.cpf}: ")
        
        if validar_cpf(novo_cpf):
            cliente.nome = novo_nome
            cliente.cpf = novo_cpf
            salvar_dados("clientes.txt", [cliente.to_dict() for cliente in clientes])
            print("Cliente alterado com sucesso!")
        else:
            print("CPF inválido! Alteração não realizada.")
    else:
        print("Cliente não encontrado!")

# Consulta de Clientes
def menu_consultar_clientes():
    print("\nLista de Clientes Cadastrados:")
    for cliente in clientes:
        print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome} | CPF: {cliente.cpf}")

# Remoção de Cliente
def menu_remover_cliente():
    cliente_id = input("ID do Cliente a ser removido: ")
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    
    if cliente:
        clientes.remove(cliente)
        salvar_dados("clientes.txt", [cliente.to_dict() for cliente in clientes])
        print(f"Cliente {cliente.nome} removido com sucesso!")
    else:
        print("Cliente não encontrado!")

# Menu de Agências (Inserção, Alteração, Consulta, Remoção)
def menu_agencias():
    while True:
        print("\nMenu de Agências")
        print("1. Inserção de Agência")
        print("2. Alteração de Agência")
        print("3. Consulta de Agência")
        print("4. Remoção de Agência")
        print("5. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_inserir_agencia()
        elif opcao == "2":
            menu_alterar_agencia()
        elif opcao == "3":
            menu_consultar_agencias()
        elif opcao == "4":
            menu_remover_agencia()
        elif opcao == "5":
            break
        else:
            print("Opção inválida! Tente novamente.")

# Inserção de Agência
def menu_inserir_agencia():
    nome = input("Nome da agência: ")
    endereco = input("Endereço da agência: ")
    agencia = Agencia(nome, endereco)
    agencias.append(agencia)
    salvar_dados("agencias.txt", [agencia.to_dict() for agencia in agencias])
    print(f"Agência {nome} cadastrada com sucesso!")

# Alteração de Agência
def menu_alterar_agencia():
    agencia_codigo = input("Código da Agência a ser alterada: ")
    agencia = next((ag for ag in agencias if ag.codigo == agencia_codigo), None)
    
    if agencia:
        novo_nome = input(f"Novo nome para a agência {agencia.nome}: ")
        novo_endereco = input(f"Novo endereço para a agência {agencia.endereco}: ")
        agencia.nome = novo_nome
        agencia.endereco = novo_endereco
        salvar_dados("agencias.txt", [agencia.to_dict() for agencia in agencias])
        print("Agência alterada com sucesso!")
    else:
        print("Agência não encontrada!")

# Consulta de Agências
def menu_consultar_agencias():
    print("\nLista de Agências Cadastradas:")
    for agencia in agencias:
        print(f"Código: {agencia.codigo} | Nome: {agencia.nome} | Endereço: {agencia.endereco}")

# Remoção de Agência
def menu_remover_agencia():
    agencia_codigo = input("Código da Agência a ser removida: ")
    agencia = next((ag for ag in agencias if ag.codigo == agencia_codigo), None)
    
    if agencia:
        agencias.remove(agencia)
        salvar_dados("agencias.txt", [agencia.to_dict() for agencia in agencias])
        print(f"Agência {agencia.nome} removida com sucesso!")
    else:
        print("Agência não encontrada!")

# Menu de Contas (Cadastro, Saldo e Extrato)
def menu_contas():
    while True:
        print("\nMenu de Contas")
        print("1. Cadastro de Contas")
        print("2. Consulta de Saldo")
        print("3. Consulta de Extrato")
        print("4. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_inserir_conta()
        elif opcao == "2":
            menu_consultar_saldo()
        elif opcao == "3":
            menu_consultar_extrato()
        elif opcao == "4":
            break
        else:
            print("Opção inválida! Tente novamente.")

# (Adapte as funções de Cadastro de Contas, Consulta de Saldo e Extrato conforme necessário)

# Menu de Movimentações (Entradas, Saídas, Saldos)
def menu_movimentos():
    while True:
        print("\nMenu de Movimentações")
        print("1. Entradas")
        print("2. Saídas")
        print("3. Saldos Anteriores e Atuais")
        print("4. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_entradas()
        elif opcao == "2":
            menu_saidas()
        elif opcao == "3":
            menu_saldos()
        elif opcao == "4":
            break
        else:
            print("Opção inválida! Tente novamente.")

# Salvar e carregar dados das listas de clientes e agências
# Isso deve ser feito para garantir persistência entre as execuções
