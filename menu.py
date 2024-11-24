from cliente import Cliente
from agencia import Agencia
from conta import ContaCorrente
from persistencia import salvar_dados, carregar_dados
from movimento import Movimento
import os
import re

# Função para verificar se os arquivos existem, caso contrário, cria-os
def verificar_arquivos():
    arquivos = ['clientes.txt', 'agencias.txt', 'contas.txt', 'movimentos.txt']
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w') as f:
                print(f"{arquivo} não existia e foi criado com sucesso.")
                pass  # Cria o arquivo vazio

verificar_arquivos()

# Listas para armazenar clientes, agências, contas e movimentações
clientes = carregar_dados("clientes.txt", Cliente)
agencias = carregar_dados("agencias.txt", Agencia)
contas = carregar_dados("contas.txt", ContaCorrente)
movimentos = carregar_dados("movimentos.txt", Movimento)

# Função de validação de data
def validar_data(data):
    # Regex para validar a data no formato dd/mm/aaaa
    padrao = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
    return bool(re.match(padrao, data))

# Função para validar o CPF
def validar_cpf(cpf):
    if re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
        return True
    return False

# Função de validação de telefone (fixo ou celular)
def validar_telefone(telefone):
    # Regex para validar números de telefone no formato brasileiro
    padrao = r"^\(\d{2}\)\s\d{4,5}-\d{4}$"
    return bool(re.match(padrao, telefone))

# Função para validar o ID de cliente e agência
def validar_cliente_agencia(cliente_id, agencia_id):
    cliente = next((cl for cl in clientes if cl.id_cliente == cliente_id), None)
    agencia = next((ag for ag in agencias if ag.codigo == agencia_id), None)
    if cliente and agencia:
        return True, cliente, agencia
    else:
        return False, None, None

# Função para exibir o menu principal
def menu_principal():
    while True:
        # Cabeçalho com borda de asteriscos e texto centralizado
        print(f"\n{'Menu Principal do Sistema Bancário':^50}")
        print("-" * 50)

        print("1. Menu de Clientes".ljust(30), "======> Opção 1")  # ljust Alinha o texto
        print("2. Menu de Agências".ljust(30), "======> Opção 2")
        print("3. Menu de Contas".ljust(30), "======> Opção 3")
        print("4. Menu de Movimentações".ljust(30), "======> Opção 4")
        print("5. Sair do Programa".ljust(30), "======> Opção 5")

        print("-" * 50)

        opcao = input("Escolha uma opção: ")
        print("=" * 50)

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
        # Cabeçalho com borda de asteriscos e texto centralizado
        print(f"\n{'Menu de Clientes':^50}")
        print("-" * 50)

        # Opções do menu com borda de igual e espaçamento
        print("1. Inserção de Cliente".ljust(30), "======> Opção 1")
        print("2. Alteração de Cliente".ljust(30), "======> Opção 2")
        print("3. Consulta de Clientes".ljust(30), "======> Opção 3")
        print("4. Remoção de Cliente".ljust(30), "======> Opção 4")
        print("5. Voltar ao Menu Principal".ljust(30), "======> Opção 5")

        # Rodapé com borda de asteriscos
        print("-" * 50)

        opcao = input("Escolha uma opção: ")
        print("=" * 50)

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

def alterar_dado(campo, nome_campo, valor_atual, cliente_nome=None, validar_funcao=None, formato=None):
    # Verifica se o campo sendo alterado é o nome ou outro campo
    if nome_campo.lower() == "nome":
        # Para o nome, não repete o nome duas vezes
        alterar = input(f"Deseja alterar o {nome_campo} de {valor_atual}? (s/n): ").strip().lower()
    else:
        # Para os outros campos, a mensagem exibe o valor atual com o nome do cliente
        if cliente_nome:
            alterar = input(f"Deseja alterar o {nome_campo}: {valor_atual} de {cliente_nome}? (s/n): ").strip().lower()
        else:
            alterar = input(f"Deseja alterar o {nome_campo}: {valor_atual}? (s/n): ").strip().lower()
    
    # Se a resposta for "sim", pede o novo valor
    if alterar == "s":
        while True:
            novo_valor = input(f"Novo {nome_campo} para {valor_atual}: ")
            # Se houver uma função de validação, ela será aplicada
            if validar_funcao:
                if validar_funcao(novo_valor):  # Aplica a validação
                    return novo_valor
                else:
                    print(f"{nome_campo} inválido! Tente novamente.")
            else:
                return novo_valor
    # Caso o usuário não queira alterar, retorna o valor atual
    return valor_atual

# Consulta de Clientes
def menu_consultar_clientes():
    print("\nLista de Clientes Cadastrados:")
    if clientes:
        for cliente in clientes:
            # Exibe os dados de forma alinhada
            print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome:<20} | CPF: {cliente.cpf} | Telefone: {cliente.telefone} | Endereço: {cliente.endereco} | Data Nascimento: {cliente.data_nascimento}")
    else:
        print("Nenhum cliente cadastrado.")
    
    input("\nPressione Enter para continuar...")  # Pausa até pressionar Enter

# Inserção de Cliente
def menu_inserir_cliente():
    nome = input("Nome do cliente: ")
    
    while True:  # Loop até o CPF ser válido
        cpf = input("CPF do cliente (formato: xxx.xxx.xxx-xx): ")
        if validar_cpf(cpf):
            break  # Sai do loop se o CPF for válido
        else:
            print("CPF inválido! Tente novamente.")
    
    while True:  # Loop até o telefone ser válido
        telefone = input("Telefone do cliente (formato: CEL (XX) XXXXX-XXXX ou TEL (XX) XXXX-XXXX): ")
        if validar_telefone(telefone):
            break  # Sai do loop se o telefone for válido
        else:
            print("Telefone inválido! Tente novamente.")
    
    endereco = input("Endereço do cliente: ")
    
    # Validação de data de nascimento
    while True:
        data_nascimento = input("Data de Nascimento do cliente (dd/mm/aaaa): ")
        if validar_data(data_nascimento):
            break  # Sai do loop se a data for válida
        else:
            print("Data de nascimento inválida! Formato esperado: dd/mm/aaaa")
    
    # Cria um novo cliente
    cliente = Cliente(str(len(clientes) + 1), nome, cpf, telefone, endereco, data_nascimento)
    clientes.append(cliente)
    
    salvar_dados("clientes.txt", clientes, sobrescrever=True)
    print(f"Cliente {nome} cadastrado com sucesso!")
    input("\nPressione Enter para continuar...")

# Alteração de Cliente - Refatorado com função genérica
def menu_alterar_cliente():
    menu_consultar_clientes()
    cliente_id = input("\nID do Cliente a ser alterado: ")
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    
    if cliente:
        cliente.nome = alterar_dado("nome", "nome", cliente.nome)
        cliente.cpf = alterar_dado("CPF", "CPF", cliente.cpf, validar_cpf)
        cliente.telefone = alterar_dado("telefone", "telefone", cliente.telefone, validar_telefone)
        cliente.endereco = alterar_dado("endereço", "endereço", cliente.endereco)
        cliente.data_nascimento = alterar_dado("data de nascimento", "data de nascimento", cliente.data_nascimento, validar_data)

        salvar_dados("clientes.txt", clientes, sobrescrever=True)
        print(f"Dados do(a) cliente {cliente.nome} alterados com sucesso!")
    else:
        print("Cliente não encontrado!")

    input("\nPressione Enter para continuar...")

# Remoção de Cliente - Refatorada para simplificar
def menu_remover_cliente():
    while True:
        menu_consultar_clientes()
        
        if not clientes:  # Verifica se há clientes na lista
            print("Não há clientes cadastrados. Retornando ao menu...")
            break  # Sai do loop se não houver clientes

        while True:  # Loop para solicitar o ID até o cliente ser encontrado
            cliente_id = input("\nID do Cliente a ser removido: ")
            cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
            
            if cliente:
                remover_cliente(cliente_id)  # Passa apenas o cliente_id
                break  # Sai do loop interno após a remoção
            else:
                print("Cliente não encontrado! Tente novamente.")  # Solicita novo ID

        break  # Sai do loop principal após a remoção

    input("\nPressione Enter para continuar...")  # Pausa até pressionar Enter

# Função para remover o cliente com o cliente_id
def remover_cliente(cliente_id):
    cliente_a_remover = next((cl for cl in clientes if cl.id_cliente == cliente_id), None)
    
    if cliente_a_remover:
        certeza_remover = input(f"Você quer realmente remover o(a) cliente: {cliente_a_remover.nome} (s/n): ").strip().lower()

        if certeza_remover == "s":
            clientes.remove(cliente_a_remover)
            print(f"Cliente {cliente_a_remover.nome} removido com sucesso.")

            # Chama salvar_dados passando o parâmetro sobrescrever=True
            salvar_dados("clientes.txt", clientes, sobrescrever=True)  # Atualiza os dados no arquivo com sobrescrição
        else:
            print("Remoção cancelada.")
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
