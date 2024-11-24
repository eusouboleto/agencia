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

# Menu Clientes
def menu_clientes():
    print("\nMenu de Cadastro de Clientes")
    nome = input("Nome do cliente: ")
    
    while True:
        cpf = input("CPF do cliente (formato: xxx.xxx.xxx-xx): ")
        if validar_cpf(cpf):
            break
        else:
            print("CPF inválido! Tente novamente.")
    
    cliente = Cliente(str(len(clientes) + 1), nome, cpf)
    clientes.append(cliente)
    
    # Salvar os dados no arquivo
    salvar_dados("clientes.txt", [cliente.to_dict() for cliente in clientes])
    print(f"Cliente {nome} cadastrado com sucesso!\n")
    
    # Exibir lista de todos os clientes
    print("Lista de todos os clientes cadastrados:")
    for cliente in clientes:
        print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome} | CPF: {cliente.cpf}")

# Menu de Cadastro de Agências
def menu_agencias():
    print("\nMenu de Cadastro de Agências")
    nome = input("Nome da agência: ")
    endereco = input("Endereço da agência: ")
    agencia = Agencia(nome, endereco)
    agencias.append(agencia)
    salvar_dados("agencias.txt", [agencia.to_dict() for agencia in agencias])
    print(f"Agência {nome} cadastrada com sucesso!")
    print("Lista de todas as agências cadastradas:")
    for agencia in agencias:
        print(f"ID_Agência: {agencia.codigo} | Nome: {agencia.nome} | Endereço: {agencia.endereco}")

# Menu de Cadastro de Contas
def menu_contas():
    print("\nMenu de Cadastro de Contas")
    numero = input("Número da Conta: ")
    cliente_id = input("ID do Cliente: ")
    agencia_id = input("ID da Agência: ")

    cliente, agencia = validar_cliente_agencia(cliente_id, agencia_id)

    if cliente and agencia:
        conta = ContaCorrente(numero, cliente, agencia, saldo_inicial=0)
        contas.append(conta)
        salvar_dados("contas.txt", [conta.to_dict() for conta in contas])
        print(f"Conta número {numero} cadastrada com sucesso!")
        print("Lista de todas as contas cadastradas:")
        for conta in contas:
            print(f"Nº da conta: {conta.numero} | Cliente: {conta.cliente.nome} | Agência: {conta.agencia.nome}")
    else:
        print("Cliente ou Agência não encontrados!")

# Menu de Movimentações
def menu_movimentos():
    print("\nMenu de Movimentações")
    numero_conta = input("Número da conta para movimentações: ")
    conta = next((c for c in contas if c.numero == numero_conta), None)
    
    if conta:
        opcao = input("Escolha uma opção:\n1. Depositar\n2. Sacar\n")
        try:
            valor = float(input("Valor: "))
        except ValueError:
            print("Valor inválido! Digite um número.")
            return
        
        if opcao == "1":
            conta.depositar(valor)
        elif opcao == "2":
            conta.sacar(valor)
        else:
            print("Opção inválida.")
            return

        print(f"Movimentação realizada com sucesso!\nSaldo atual: {conta.saldo}")
        print("Extrato da conta:")
        for mov in conta.get_extrato():
            print(f"{mov.tipo}: {mov.valor}")
        
        salvar_dados("movimentos.txt", [mov.to_dict() for mov in conta.get_extrato()])
    else:
        print("Conta não encontrada!")

# Função para carregar dados de arquivos e inicializar as listas
def cadastro_padrao():
    global clientes, agencias, contas  # Declarar as variáveis como globais

    # Carregar dados de clientes, agências e contas se existirem
    clientes_dados = carregar_dados("clientes.txt")
    clientes.extend([Cliente.from_dict(dado) for dado in clientes_dados if Cliente.from_dict(dado) is not None])

    agencias_dados = carregar_dados("agencias.txt")
    agencias.extend([Agencia.from_dict(dado) for dado in agencias_dados if Agencia.from_dict(dado) is not None])

    contas_dados = carregar_dados("contas.txt")
    contas.extend([ContaCorrente.from_dict(dado) for dado in contas_dados if ContaCorrente.from_dict(dado) is not None])

    # Dados padrão, caso a lista esteja vazia
    if not clientes:
        cliente1 = Cliente("1", "João Silva", "123.456.789-00")
        cliente2 = Cliente("2", "Maria Oliveira", "234.567.890-11")
        salvar_dados("clientes.txt", [cliente1.to_dict(), cliente2.to_dict()])
        clientes.extend([cliente1, cliente2])  # Adiciona à lista, sem substituir

    if not agencias:
        agencia1 = Agencia("001", "Rua A, 100")
        agencia2 = Agencia("002", "Avenida B, 200")
        salvar_dados("agencias.txt", [agencia1.to_dict(), agencia2.to_dict()])
        agencias.extend([agencia1, agencia2])  # Adiciona à lista, sem substituir

    if not contas:
        conta1 = ContaCorrente("1001", clientes[0], agencias[0], 1000)
        conta2 = ContaCorrente("1002", clientes[1], agencias[1], 2000)
        salvar_dados("contas.txt", [conta1.to_dict(), conta2.to_dict()])
        contas.extend([conta1, conta2])  # Adiciona à lista, sem substituir