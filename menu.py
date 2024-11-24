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

def validar_cnpj(cnpj):
    # Remove espaços em branco e qualquer pontuação do CNPJ
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    # Verifica se o CNPJ tem 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se o CNPJ não é composto por todos os mesmos dígitos (ex: 11111111111111)
    if cnpj == cnpj[0] * 14:
        return False
    
    return True

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

def alterar_dado(campo, nome_campo, valor_atual, cliente_nome=None, agencia_nome=None, validar_funcao=None, formato=None):
    # Mensagem de confirmação de alteração
    if cliente_nome:
        alterar = input(f"Deseja alterar o {nome_campo}: {valor_atual} de {cliente_nome}? (s/n): ").strip().lower()
    elif agencia_nome:
        # Exibe o valor atual de cada campo de agência para confirmar a alteração
        alterar = input(f"Deseja alterar o {nome_campo}: {valor_atual} da agência {agencia_nome}? (s/n): ").strip().lower()
    else:
        alterar = input(f"Deseja alterar o {nome_campo}: {valor_atual}? (s/n): ").strip().lower()

    # Se a resposta for "sim", pede o novo valor
    if alterar == "s":
        while True:
            novo_valor = input(f"Novo {nome_campo} para {valor_atual}: ")
            
            # Validação do novo valor, se houver função de validação
            if validar_funcao:
                if validar_funcao(novo_valor):  # Se a validação for bem-sucedida
                    return novo_valor
                else:
                    print(f"{nome_campo.capitalize()} inválido! Tente novamente.")
            else:
                return novo_valor
    # Caso não altere o valor, retorna o valor atual
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

def menu_alterar_cliente():
    menu_consultar_clientes()
    cliente_id = input("\nID do Cliente a ser alterado: ")
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    
    if cliente:
        cliente.nome = alterar_dado("nome", "nome", cliente.nome)
        cliente.cpf = alterar_dado("CPF", "CPF", cliente.cpf, cliente.nome, validar_cpf)
        cliente.telefone = alterar_dado("telefone", "telefone", cliente.telefone, cliente.nome, validar_telefone)
        cliente.endereco = alterar_dado("endereço", "endereço", cliente.endereco, cliente.nome)
        cliente.data_nascimento = alterar_dado("data de nascimento", "data de nascimento", cliente.data_nascimento, cliente.nome, validar_data)

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

def menu_agencias():
    while True:
        # Cabeçalho com borda de asteriscos e texto centralizado
        print(f"\n{'Menu de Agências':^50}")
        print("-" * 50)

        print("1. Inserção de Agência".ljust(30), "======> Opção 1")
        print("2. Alteração de Agência".ljust(30), "======> Opção 2")
        print("3. Consulta de Agência".ljust(30), "======> Opção 3")
        print("4. Remoção de Agência".ljust(30), "======> Opção 4")
        print("5. Voltar ao Menu Principal".ljust(30), "======> Opção 5")

        print("-" * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_inserir_agencia()
        elif opcao == "2":
            menu_alterar_agencia()
        elif opcao == "3":
            menu_consultar_agencias()
        elif opcao == "4":
            menu_remover_agencia()
        elif opcao == "5":
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Inserção de Agência
def menu_inserir_agencia():
    print(f"\n{'Inserir Nova Agência':^50}")
    print("-" * 50)

    nome = input("Nome da agência: ").strip()
    endereco = input("Endereço da agência: ").strip()

    # Validação de CNPJ
    while True:
        cnpj = input("CNPJ da agência (formato: XX.XXX.XXX/XXXX-XX): ").strip()
        if validar_cnpj(cnpj):
            # Verifica se o CNPJ já existe
            if any(agencia.cnpj == cnpj for agencia in agencias):
                print("Erro: Já existe uma agência cadastrada com este CNPJ!")
            else:
                break
        else:
            print("CNPJ inválido! Tente novamente.")

    # Validação de telefone
    while True:
        telefone = input("Telefone da agência (formato: TEL (XX) XXXX-XXXX): ").strip()
        if validar_telefone(telefone):
            break
        else:
            print("Telefone inválido! Tente novamente.")

    # Criação e salvamento da nova agência
    try:
        # Gerando o ID da agência baseado no tamanho da lista
        id_agencia = len(agencias) + 1
        nova_agencia = Agencia(id_agencia, nome, endereco, cnpj, telefone)
        agencias.append(nova_agencia)
        
        salvar_dados("agencias.txt", agencias, sobrescrever=True)
        print(f"Agência '{nome}' cadastrada com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar agência: {e}")

    input("\nPressione Enter para continuar...")


def menu_alterar_agencia():
    menu_consultar_agencias()
    # Solicita o código da agência a ser alterada
    agencia_codigo = input("Código da Agência a ser alterada: ")
    
    # Encontra a agência correspondente
    agencia = next((ag for ag in agencias if ag.id_agencia == agencia_codigo), None)
    
    if agencia:
        # Alteração do nome
        agencia.nome = alterar_dado("nome", "nome", agencia.nome)
        
        # Alteração do endereço
        agencia.endereco = alterar_dado("endereço", "endereço", agencia.endereco, agencia.nome)
        
        # Alteração do CNPJ (validação opcional)
        agencia.cnpj = alterar_dado("CNPJ", "CNPJ", agencia.cnpj, agencia.nome, validar_cnpj)
        
        # Alteração do telefone (validação opcional)
        agencia.telefone = alterar_dado("telefone", "telefone", agencia.telefone, agencia.nome, validar_telefone)
        
        # Salva os dados após a alteração
        salvar_dados("agencias.txt", agencias, sobrescrever=True)
        print(f"Dados da agência {agencia.nome} alterados com sucesso!")
    else:
        print("Agência não encontrada!")

    input("\nPressione Enter para continuar...")


# Consulta de Agências
def menu_consultar_agencias():
    print("\nLista de Agências Cadastradas:")
    if agencias:
        for agencia in agencias:
            # Exibe os dados de forma alinhada
            print(f"Código: {agencia.id_agencia} | Nome: {agencia.nome:<20} | Endereço: {agencia.endereco}")
    else:
        print("Nenhuma agência cadastrada.")
    
    input("\nPressione Enter para continuar...")  # Pausa até pressionar Enter


# Remoção de Agência - Refatorada para simplificar
def menu_remover_agencia():
    while True:
        menu_consultar_agencias()

        if not agencias:  # Verifica se há agências na lista
            print("Não há agências cadastradas. Retornando ao menu...")
            break  # Sai do loop se não houver agências

        while True:  # Loop para solicitar o código da agência até a agência ser encontrada
            agencia_codigo = input("\nCódigo da Agência a ser removida: ")
            agencia = next((ag for ag in agencias if ag.id_agencia == agencia_codigo), None)
            
            if agencia:
                agencias.remove(agencia)  # Remove a agência
                salvar_dados("agencias.txt", [agencia.to_dict() for agencia in agencias])  # Atualiza os dados
                print(f"Agência {agencia.nome} removida com sucesso!")
                break  # Sai do loop interno após a remoção
            else:
                print("Agência não encontrada! Tente novamente.")  # Solicita novo código

        break  # Sai do loop principal após a remoção

    input("\nPressione Enter para continuar...")  # Pausa até pressionar Enter

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
