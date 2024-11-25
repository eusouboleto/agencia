from cliente import Cliente
from agencia import Agencia
from conta import Conta, ContaEspecial, ContaCorrente
from persistencia import salvar_dados, carregar_dados, proximo_id_disponivel, remover_por_id
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

# Carregar todas as contas e depois separá-las
contas = carregar_dados("contas.txt", Conta)  # Carrega todas as contas
contas_corrente = [conta for conta in contas if isinstance(conta, ContaCorrente)]  # Filtra as contas correntes
contas_especial = [conta for conta in contas if isinstance(conta, ContaEspecial)]  # Filtra as contas especiais

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

def menu_remover(tipo_item, nome_arquivo):
    """
    Menu genérico para remover um objeto (Cliente, Agência, etc.) de um arquivo.
    Args:
        tipo_item (class): Classe do objeto (ex: Cliente, Agencia).
        nome_arquivo (str): Nome do arquivo onde os dados estão armazenados (ex: "clientes.txt").
    """
    while True:
        # Verifica se o arquivo existe antes de tentar carregar os dados
        if not verificar_arquivo(nome_arquivo):
            print(f"O arquivo {nome_arquivo} não existe. Retornando ao menu...")
            break  # Sai do loop se o arquivo não existir

        # Exibe os itens cadastrados
        print(f"\nLista de {tipo_item.__name__}s Cadastrados:")
        itens = carregar_dados(nome_arquivo, tipo_item)
        
        if not itens:
            print(f"Não há {tipo_item.__name__}s cadastrados. Retornando ao menu...")
            break  # Sai do loop se não houver itens

        for item in itens:
            print(item.to_string())

        while True:
            try:
                id_item = int(input(f"\nID do {tipo_item.__name__} a ser removido: "))
                remover_por_id(nome_arquivo, tipo_item, id_item)
                break  # Sai do loop interno após a remoção
            except ValueError:
                print("ID inválido! Tente novamente.")  # Solicita novo ID

        break  # Sai do loop principal após a remoção

    input("\nPressione Enter para continuar...")  # Pausa até pressionar Enter

def verificar_arquivo(nome_arquivo):
    """
    Verifica se um arquivo existe.
    Args:
        nome_arquivo (str): Nome do arquivo a ser verificado.
    Returns:
        bool: True se o arquivo existir, False caso contrário.
    """
    try:
        with open(nome_arquivo, 'r'):
            return True
    except FileNotFoundError:
        return False

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
        
    id_cliente = proximo_id_disponivel("clientes.txt", Cliente)
    
    # Cria um novo cliente
    cliente = Cliente(id_cliente, nome, cpf, telefone, endereco, data_nascimento)
    clientes.append(cliente)
    
    salvar_dados("clientes.txt", clientes, sobrescrever=True)
    print(f"Cliente {nome} cadastrado com sucesso!")
    input("\nPressione Enter para continuar...")

def menu_alterar_cliente():
    menu_consultar_clientes()

    # Solicita o ID do cliente a ser alterado
    cliente_id = input("\nID do Cliente a ser alterado: ")
    
    # Localiza o cliente a partir do ID
    cliente = next((c for c in clientes if str(c.id_cliente) == str(cliente_id)), None)
    
    if cliente:
        # Alteração dos dados do cliente
        cliente.nome = alterar_dado("nome", "nome", cliente.nome)
        cliente.cpf = alterar_dado("CPF", "CPF", cliente.cpf, cliente.nome, validar_cpf)
        cliente.telefone = alterar_dado("telefone", "telefone", cliente.telefone, cliente.nome, validar_telefone)
        cliente.endereco = alterar_dado("endereço", "endereço", cliente.endereco, cliente.nome)
        cliente.data_nascimento = alterar_dado("data de nascimento", "data de nascimento", cliente.data_nascimento, cliente.nome, validar_data)

        # Salva os dados do cliente após a alteração
        salvar_dados("clientes.txt", clientes, sobrescrever=True)
        print(f"Dados do(a) cliente {cliente.nome} alterados com sucesso!")
    else:
        print("Cliente não encontrado!")

    input("\nPressione Enter para continuar...")

def menu_remover_cliente():
    # Exibe a lista de clientes cadastrados
    menu_consultar_clientes()

    # Solicita o ID do cliente a ser removido
    cliente_id = input("\nID do Cliente a ser removido: ").strip()

    # Tenta converter o ID para inteiro (caso seja um número)
    try:
        cliente_id = int(cliente_id)
    except ValueError:
        print(f"O ID fornecido ({cliente_id}) não é válido. Por favor, insira um número inteiro.")
        return

    # Encontra o cliente correspondente
    cliente = next((c for c in clientes if c.id_cliente == cliente_id), None)
    
    if cliente:
        # Exibe os detalhes do cliente para confirmação
        print(f"\nVocê quer realmente remover o(a) Cliente: {cliente.nome} (ID: {cliente.id_cliente})?")
        print(cliente.to_string())  # Mostra o cliente com todos os dados

        # Confirma a remoção do cliente
        remover = input("(s/n): ").strip().lower()
        
        if remover == "s":
            # Remove o cliente da lista
            clientes.remove(cliente)
            # Salva os dados atualizados no arquivo
            salvar_dados("clientes.txt", clientes, sobrescrever=True)
            print("Cliente removido com sucesso.")
        else:
            print("Remoção cancelada.")
    else:
        print(f"Cliente com ID {cliente_id} não encontrado!")
    
    input("\nPressione Enter para continuar...")


def remover_cliente(cliente_id):
    # Carrega os dados do arquivo para garantir que estão atualizados
    clientes = carregar_dados("clientes.txt", Cliente)

    # Localiza o cliente pelo ID
    cliente_a_remover = next((cl for cl in clientes if cl.id_cliente == cliente_id), None)

    if cliente_a_remover:
        # Confirmação antes de remover
        certeza_remover = input(f"Você quer realmente remover o(a) cliente: {cliente_a_remover.nome} (s/n): ").strip().lower()

        if certeza_remover == "s":
            # Remove o cliente da lista
            clientes.remove(cliente_a_remover)
            print(f"Cliente {cliente_a_remover.nome} removido com sucesso.")

            # Salva os dados atualizados no arquivo
            salvar_dados("clientes.txt", clientes, sobrescrever=True)
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
        id_agencia = proximo_id_disponivel("agencias.txt", Agencia)
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
    agencia_codigo = input("\nCódigo da Agência a ser alterada: ")
    
    # Localiza a agência a partir do ID
    agencia = next((ag for ag in agencias if str(ag.id_agencia) == str(agencia_codigo)), None)
    
    if agencia:
        # Alteração dos dados da agência
        agencia.nome = alterar_dado("nome", "nome", agencia.nome)
        agencia.endereco = alterar_dado("endereço", "endereço", agencia.endereco, agencia.nome)
        agencia.cnpj = alterar_dado("CNPJ", "CNPJ", agencia.cnpj, agencia.nome, validar_cnpj)
        agencia.telefone = alterar_dado("telefone", "telefone", agencia.telefone, agencia.nome, validar_telefone)
        
        # Salva os dados da agência após a alteração
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


def menu_remover_agencia():
    menu_consultar_agencias()

    # Solicita o ID da agência a ser removido
    agencia_id = input("\nID da Agência a ser removido: ")
    
    # Tenta converter o ID para inteiro (caso seja um número)
    try:
        agencia_id = int(agencia_id)
    except ValueError:
        print(f"O ID fornecido ({agencia_id}) não é válido. Por favor, insira um número inteiro.")
        return
    
    # Encontra a agência correspondente
    agencia = next((a for a in agencias if a.id_agencia == agencia_id), None)
    
    if agencia:
        # Exibe as informações da agência e solicita a confirmação para remoção
        print(f"Você quer realmente remover o(a) Agencia com ID {agencia_id}?")
        print(agencia)  # Agora exibe as informações legíveis da agência
        
        remover = input("(s/n): ").strip().lower()
        
        if remover == "s":
            # Remove a agência da lista
            agencias.remove(agencia)
            # Salva os dados atualizados no arquivo
            salvar_dados("agencias.txt", agencias, sobrescrever=True)
            print("Agência removida com sucesso.")
        else:
            print("Remoção cancelada.")
    else:
        print(f"Agência com ID {agencia_id} não encontrada!")
    
    input("\nPressione Enter para continuar...")

# Menu de Contas (Cadastro, Saldo e Extrato)
def menu_contas():
    while True:
        # Cabeçalho com borda de asteriscos e texto centralizado
        print(f"\n{'Menu de Contas':^50}")
        print("-" * 50)

        print("1. Cadastro de Conta".ljust(30), "======> Opção 1")
        print("2. Consulta de Saldo".ljust(30), "======> Opção 2")
        print("3. Consulta de Extrato".ljust(30), "======> Opção 3")
        print("4. Voltar ao Menu Principal".ljust(30), "======> Opção 4")

        print("-" * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_inserir_conta()
        elif opcao == "2":
            menu_consultar_saldo()
        elif opcao == "3":
            pass #menu_consultar_extrato()
        elif opcao == "4":
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Inserção de conta
def menu_inserir_conta():
    print(f"\n{'Inserir Nova Conta':^50}")
    print("-" * 50)

    numero = input("Número da conta: ").strip()

    # Verificar se o número da conta já existe
    if any(conta.numero == numero for conta in contas):
        print(f"Erro: A conta {numero} já existe! Escolha outro número.")
        return

    # Exibir as agências disponíveis através da função menu_consultar_agencias
    menu_consultar_agencias()

    while True:
        try:
            codigo_agencia = int(input(f"\nDigite o código da agência para a conta {numero}: ").strip())
            agencia = next((ag for ag in agencias if ag.id_agencia == codigo_agencia), None)

            if agencia:
                # Exibir os clientes disponíveis
                menu_consultar_clientes()

                while True:
                    try:
                        # Solicitar ID do cliente
                        id_cliente = int(input("\nDigite o ID do cliente para associar à conta: ").strip())
                        cliente = next((c for c in clientes if c.id_cliente == id_cliente), None)

                        if cliente:
                            break
                        else:
                            print("Cliente não encontrado. Tente novamente.")
                    except ValueError:
                        print("ID inválido! Tente novamente.")

                # Confirmar se o cliente quer mesmo adicionar o cliente à agência
                print(f"\nVocê selecionou a agência {agencia.id_agencia} - {agencia.nome}.")
                print(f"Cliente: {cliente.nome} (ID: {cliente.id_cliente})")
                
                confirmacao = input("Tem certeza que deseja associar este cliente a esta agência? (s/n): ").strip().lower()

                if confirmacao == 's':
                    break
                elif confirmacao == 'n':
                    print("Operação cancelada. Retornando ao Menu de Contas.")
                    return
                else:
                    print("Opção inválida! Digite 's' para sim ou 'n' para não.")
            else:
                print("Agência não encontrada. Tente novamente.")

        except ValueError:
            print("Código inválido! Digite um número.")

    # Escolher o tipo de conta (Corrente ou Especial)
    while True:
        tipo_conta = input("\nEscolha o tipo de conta (1 - Corrente, 2 - Especial): ").strip()
        if tipo_conta in ['1', '2']:
            break
        else:
            print("Opção inválida! Digite 1 para Corrente ou 2 para Especial.")

    # Solicitar saldo inicial
    while True:
        try:
            saldo_inicial = float(input("Saldo inicial da conta: R$ ").strip())
            if saldo_inicial >= 0:
                break
            else:
                print("O saldo inicial não pode ser negativo! Tente novamente.")
        except ValueError:
            print("Valor inválido para o saldo! Tente novamente.")

    # Gerar a conta de acordo com o tipo selecionado
    if tipo_conta == '1':  # Conta Corrente
        conta = ContaCorrente(numero, cliente, agencia, saldo_inicial)
    else:  # Conta Especial
        conta = ContaEspecial(numero, cliente, agencia, saldo_inicial)

    # Adicionar a conta à lista de contas
    contas.append(conta)

    # Salvar dados da conta no arquivo
    try:
        salvar_dados("contas.txt", [conta], sobrescrever=False)  # Passando apenas a conta criada
        print(f"Conta {numero} cadastrada com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar conta: {e}")

    input("\nPressione Enter para continuar...")

# Consultar saldo
def menu_consultar_saldo():
    print(f"\n{'Consultar Saldo':^50}")
    print("-" * 50)

    # Exibir as contas disponíveis
    if not contas:
        print("Não há contas cadastradas no sistema.")
        input("\nPressione Enter para continuar...")
        return

    print("Contas cadastradas:")
    for conta in contas:
        print(f"Conta: {conta.numero} - Titular: {conta.cliente.nome}")

    # Solicitar a conta para consulta de saldo
    while True:
        numero_conta = input("\nDigite o número da conta para consultar o saldo: ").strip()
        conta = next((conta for conta in contas if conta.numero == numero_conta), None)

        if conta:
            # Exibir o saldo da conta
            print(f"\nSaldo da conta {conta.numero}: R$ {conta.saldo:.2f}")
            break
        else:
            print("Conta não encontrada. Tente novamente.")

    input("\nPressione Enter para continuar...")

# Consultar Extrato
def menu_consultar_extrato():
    print(f"\n{'Consultar Extrato':^50}")
    print("-" * 50)

    # Exibir as contas disponíveis
    if not contas:
        print("Não há contas cadastradas no sistema.")
        input("\nPressione Enter para continuar...")
        return

    print("Contas cadastradas:")
    for conta in contas:
        print(f"Conta: {conta.numero} - Titular: {conta.cliente.nome}")

    # Solicitar a conta para consulta de extrato
    while True:
        numero_conta = input("\nDigite o número da conta para consultar o extrato: ").strip()
        conta = next((conta for conta in contas if conta.numero == numero_conta), None)

        if conta:
            # Exibir o extrato da conta
            print(f"\nExtrato da conta {conta.numero}:")
            print("-" * 50)

            if not conta.movimentos:
                print("Não há movimentações nesta conta.")
            else:
                for movimento in conta.movimentos:
                    print(f"{movimento.data} - {movimento.tipo} - R$ {movimento.valor:.2f}")

            break
        else:
            print("Conta não encontrada. Tente novamente.")

    input("\nPressione Enter para continuar...")


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
