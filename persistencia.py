import os
from cliente import Cliente
from agencia import Agencia
from conta import Conta, ContaCorrente, ContaEspecial
from movimento import Movimento

def carregar_dados(nome_arquivo, tipo_item):
    lista = []
    if os.path.exists(nome_arquivo):  # Verifica se o arquivo existe
        with open(nome_arquivo, "r") as arquivo:
            dados = arquivo.readlines()
            for linha in dados:
                linha = linha.strip()  # Remove quebras de linha e espaços extras
                try:
                    # Verifica o tipo de item e chama o método estático apropriado para reconstrução
                    if tipo_item == Cliente:
                        item = Cliente.from_string(linha)
                    elif tipo_item == Agencia:
                        item = Agencia.from_string(linha)
                    elif tipo_item == ContaCorrente:
                        # A ContaCorrente possui limite, por isso pode ser identificada assim
                        if "limite" in linha:
                            item = ContaCorrente.from_string(linha)
                        else:
                            item = Conta.from_string(linha)  # Caso seja uma conta genérica
                    elif tipo_item == ContaEspecial:
                        # Verifica se é ContaEspecial, com base no campo limite
                        if "limite" in linha:
                            item = ContaEspecial.from_string(linha)
                        else:
                            item = Conta.from_string(linha)  # Caso seja uma conta genérica
                    elif tipo_item == Movimento:
                        item = Movimento.from_string(linha)
                    else:
                        print(f"Tipo desconhecido: {tipo_item}")
                        continue
                    
                    lista.append(item)
                except Exception as e:
                    print(f"Erro ao carregar a linha: '{linha}'. Erro: {e}")
    return lista


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
                elif isinstance(dado, ContaEspecial):
                    arquivo.write(dado.to_string() + "\n")
                elif isinstance(dado, Movimento):
                    arquivo.write(dado.to_string() + "\n")
                elif isinstance(dado, Conta):
                    # Ignore o dado se for uma instância genérica de Conta
                    print(f"Conta não deve ser salva diretamente. ID: {dado.numero}")
                else:
                    print(f"Tipo desconhecido: {type(dado)}")
    except Exception as e:
        print(f"Erro ao abrir ou escrever no arquivo {nome_arquivo}: {e}")

def proximo_id_disponivel(arquivo, classe):
    """
    Determina o próximo ID disponível baseado nos dados armazenados no arquivo.
    Args:
        arquivo (str): Caminho do arquivo que contém os dados.
        classe (type): Classe do objeto que será instanciado para extrair o ID.
    Returns:
        int: O próximo ID disponível.
    """
    try:
        with open(arquivo, "r") as file:
            ids_existentes = []
            for linha in file:
                # Usa from_string para reconstruir o objeto
                objeto = classe.from_string(linha.strip())
                if isinstance(objeto, Cliente):
                    ids_existentes.append(int(objeto.id_cliente))
                elif isinstance(objeto, Agencia):
                    ids_existentes.append(int(objeto.id_agencia))
            return max(ids_existentes, default=0) + 1
    except FileNotFoundError:
        return 1
    
def remover_por_id(nome_arquivo, classe, id_objeto):
    """
    Remove um objeto do arquivo baseado no ID.
    Args:
        nome_arquivo (str): Nome do arquivo onde os objetos estão salvos.
        classe (type): Classe do objeto (ex: Cliente, Agencia).
        id_objeto (int): ID do objeto a ser removido.
    """
    try:
        # Certifique-se de que o ID fornecido seja do tipo correto (inteiro)
        id_objeto = int(id_objeto)
    except ValueError:
        print(f"O ID fornecido ({id_objeto}) não é válido. Por favor, insira um número inteiro.")
        return

    # Carrega todos os objetos do arquivo
    objetos = carregar_dados(nome_arquivo, classe)
    
    # Localiza o objeto a ser removido
    objeto_a_remover = None
    for obj in objetos:
        # Verifica se o ID do objeto corresponde ao ID fornecido
        if isinstance(obj, Cliente) and obj.id_cliente == id_objeto:
            objeto_a_remover = obj
            break
        elif isinstance(obj, Agencia) and obj.id_agencia == id_objeto:
            objeto_a_remover = obj
            break
        # Adicione condições para outras classes, se necessário

    if objeto_a_remover:
        # Exibe as informações do objeto que será removido
        print(f"Objeto encontrado: {objeto_a_remover}")

        # Confirmação antes de remover
        certeza_remover = input(f"Você quer realmente remover o(a) {classe.__name__} com ID {id_objeto}? (s/n): ").strip().lower()
        
        if certeza_remover == "s":
            # Remove o objeto da lista
            objetos.remove(objeto_a_remover)
            print(f"{classe.__name__} com ID {id_objeto} removido com sucesso.")

            # Sobrescreve o arquivo com os dados atualizados
            salvar_dados(nome_arquivo, objetos, sobrescrever=True)
        else:
            print("Remoção cancelada.")
    else:
        print(f"{classe.__name__} com ID {id_objeto} não encontrado!")


def alterar_por_id(nome_arquivo, classe, id_objeto, novo_valor, campo):
    """
    Altera um campo de um objeto no arquivo baseado no ID.
    Args:
        nome_arquivo (str): Nome do arquivo onde os objetos estão salvos.
        classe (type): Classe do objeto que será instanciado para verificar o ID.
        id_objeto (int): ID do objeto a ser alterado.
        novo_valor (str): Novo valor para o campo.
        campo (str): Nome do campo a ser alterado (ex: 'nome', 'cpf', etc.)
    """
    # Certifique-se de que o ID fornecido seja do tipo correto (inteiro)
    id_objeto = int(id_objeto)

    # Carrega todos os objetos do arquivo
    objetos = carregar_dados(nome_arquivo, classe)
    
    # Localiza o objeto a ser alterado
    objeto_a_alterar = None
    for obj in objetos:
        # Verifica se o ID do objeto corresponde ao ID fornecido
        if isinstance(obj, Cliente) and obj.id_cliente == id_objeto:
            objeto_a_alterar = obj
            break
        elif isinstance(obj, Agencia) and obj.id_agencia == id_objeto:
            objeto_a_alterar = obj
            break
        # Adicione condições para outras classes, se necessário

    if objeto_a_alterar:
        # Confirmação antes de alterar
        certeza_alterar = input(f"Você quer realmente alterar o(a) {campo} de {objeto_a_alterar} para {novo_valor}? (s/n): ").strip().lower()
        
        if certeza_alterar == "s":
            # Altera o campo desejado
            setattr(objeto_a_alterar, campo, novo_valor)
            print(f"{campo} alterado com sucesso.")

            # Sobrescreve o arquivo com os dados atualizados
            salvar_dados(nome_arquivo, objetos, sobrescrever=True)
        else:
            print("Alteração cancelada.")
    else:
        print(f"{classe.__name__} com ID {id_objeto} não encontrado!")
