from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    # Atributos da classe Cliente
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    # Função realizar_transacao(self, conta, transacao)
    def realizar_transacao(self, conta, transacao):
        # Registra usando as instâncias da classe Transação dentro da conta do cliente
        transacao.registrar(conta)

    # Função adicionar_conta(self, conta)
    def adicionar_conta(self, conta):
        # Adiciona à lista de contas a conta nova
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(endereco)


class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    # Método de classe para criar uma nova conta
    @classmethod
    def nova_conta(cls, numero_conta, cliente):
        return cls(numero_conta, cliente)

    # Métodos para podermos modificar as instâncias dos objetos que são propriedade da classe Conta
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_limite = valor > saldo

        if excedeu_limite:  # Verifica se o limite foi excedido
            print("== Operação falhou ==\n== Saldo Insuficiente ==")

        elif valor > 0:  # Verifica se o valor é válido, já que a verificação excedeu_limite já aconteceu
            saldo -= valor
            print("\n=== Saque realizado com sucesso ===")
            return True

        else:
            print("== Operação Falhou ==\n== Valor Inválido ==")

        return False  # Retorna falso por padrão porque caso haja algum caso que não se encaixe dentro das nossas verificações a operação não acontecerá

    def depositar(self, valor):
        saldo = self._saldo
        if valor > 0:
            saldo += valor
            print("=== Depósito Realizado com sucesso ===")

        else:
            print("== Operação Falhou ==\n== Valor Inválido ==")

        return False  # Retorna falso por padrão porque caso haja algum caso que não se encaixe dentro das nossas verificações a operação não acontecerá


class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3, limite_tentativa_saques=3):
        super().__init__(cliente, numero_conta)
        self.limite = limite
        self.limite_saques = limite_saques
        self.limite_tentativa_saques = limite_tentativa_saques

    def saques(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        # condicional para caso exceda limite valor ou numero de saques
        if excedeu_limite:
            print("== Operação Falhou ==\n== Valor de saque excede o seu limite ==")

        elif excedeu_saques:
            print("== Operação Falhou ==\n== Limite de saques excedido ==")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
        Agência: {self.agencia}
        Número da Conta Corrente: {self.numero_conta}
        Titular da Conta: {self.cliente.nome}
        CPF do Titular da Conta: {self.cliente.cpf}
        """


class Historico:  # Classe que armazenará as transações realizadas pelo usuário
    # Atributos da classe Historico
    def __init__(self):
        # Dicionário de transações, que armazena o tipo e o valor de cada transação (saque/depósito e valor)
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        # Adiciona cada transação ao histórico
        self._transacoes.append(
            {
                # Usado para acessar a instância do nome da transação realizada
                "tipo": transacao.__class__.__name__,
                # Usado para acessar o valor da transação instanciado nas classes Deposito ou Saque
                "valor": transacao.valor,
            }
        )


class Transacao(ABC):
    @property  # Indica para as classes filhas que essa instância de classe é uma propriedade da classe pai
    @abstractmethod  # Para que todas as classes filhas sejam obrigadas a implementá-lo
    # É vazio porque o objeto será instanciado dentro da classe saque ou deposito palavra
    def valor(self):
        pass

    @abstractmethod  # Para que todas as classes filhas sejam obrigadas a implementá-lo, sem precisar colocar o decorador
    # É vazio porque o objeto será preenchido dentro da classe saque ou deposito
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    # Atributos da classe Deposito
    def __init__(self, valor):
        self._valor = valor  # Encapsulando o objeto como um método privado

    @property
    def valor(self):
        pass

    def registrar(self, conta):
        # Define o sucesso_transacao como o resultado do método depositar presente na classe Conta que retorna (T/F)
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            # Executa o método adicionar_transacao que pertence a classe Historico com as instâncias do objeto conta adicionando a transação ao dicionário _transações
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    # Atributos da classe Deposito
    def __init__(self, valor):
        self._valor = valor  # Encapsulando o objeto como um método privado

    @property
    def valor(self):
        pass

    def registrar(self, conta):
        # Define o sucesso_transacao como o resultado do método sacar presente na classe Conta que retorna (T/F)
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            # Executa o método adicionar_transacao que pertence a classe Historico com as instâncias do objeto conta adicionando a transação ao dicionário _transações
            conta.historico.adicionar_transacao(self)


def depositar(clientes):

    cpf = input("Insira seu CPF: ")
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:

        conta = verificar_conta_cliente(cliente)

        if not conta:
            return

        valor = float(input("Insira um valor para depósito: R$"))

        if valor > 0:
            transacao = Deposito(valor)
            cliente.realizar_transacao(conta, transacao)

    else:
        print("== Cliente não encontrado ==")


def sacar(clientes):
    cpf = input("Insira seu CPF: ")
    cliente = filtrar_clientes(clientes)

    if cliente:
        conta = verificar_conta_cliente(cliente)

        if not conta:
            return

        valor = input("Insira o valor que desejas sacar\n==>")
        transacao = Saque(valor)

        cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Insira seu CPF:\n==>")
    cliente = filtrar_clientes(clientes)

    if cliente:
        conta = verificar_conta_cliente(cliente)

        if not conta:
            return

        print("============== EXTRATO ==============\n")
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            print("== Não foram feitas movimentações nessa conta ==")

        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}: R${transacao['valor']:.2f}"

        print(extrato)
        print(f"Saldo: {conta.saldo:.2f}\n")
        print("=====================================")


def verificar_conta_cliente(cliente):
    if not cliente.contas:
        print("== Cliente não possui conta ==")
        return

    else:
        numero_de_conta = int(input("Qual conta desejas usar: "))
        return cliente.contas[numero_de_conta]


def filtrar_clientes(cpf, clientes):
    filtro_clientes = [cliente for cliente in clientes if cliente.cpf == cpf]

    return filtro_clientes[0] if filtro_clientes else None


def novo_cliente(clientes):
    # nome, nascimento, cpf, endereço
    cpf = input("Insira seu CPF (somente números): ")
    filtro = filtrar_clientes(cpf, clientes)

    if filtro:  # Analisa se o cpf ja está cadastrado
        print("\n== CPF já cadastrado para outro usuário ==\n== Insira um CPF novo ==\n")

    nome = input("\nInsira seu nome completo: ")
    data_nasc = input("Insira sua data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Insira seu endereço (rua, num - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(
        nome=nome, cpf=cpf, data_nascimento=data_nasc, endereco=endereco)

    clientes.append(cliente)

    print("\n== Cliente criado com sucesso! ==")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Insira seu CPF (somente números): ")
    print(cpf)
    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        # Vincula o objeto conta à classe ContaCorrente
        conta = ContaCorrente(numero_conta=numero_conta, cliente=cliente)

        # Adiciona à lista de contas a conta que acabamos de criar
        contas.append(conta)

        # Adiciona à lista de contas pessoais do cliente a nova conta
        cliente.contas.append(conta)

        print("Conta Criada com sucesso!")
        print("=================================\n")

    print("\nUsuário não encontrado. Crie um usuário primeiro para adicionar uma conta.")


def listar_contas(contas):
    for conta in contas:
        print(str(conta))


def menu():
    menu = '''    
    ============ MENU ============
            Bamko Manikômico

        [nc] Novo Cliente
        [cc] Criar Conta
        [lc] Listar Contas
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair

    ==============================
    => '''
    return input(menu)


def main():
    # Variáveis
    clientes = [{"nome": "Samuel", "data_nascimento": "30-12-2003", "cpf": "07032795307",
                 "endereco": "Rua Dom Lino, 188 - Parquelândia - Fortaleza/CE"}]
    contas = []

    # Constantes
    MENSAGEM = "\nEH U MANIKAS HEHE"

    # Estrutura Principal do Sistema
    while True:
        option = menu()

        if option == "nc":  # Novo Cliente
            novo_cliente(clientes)

        elif option == "cc":  # Criar Conta
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes)

        elif option == "lc":  # Listar Contas
            listar_contas(contas)

        elif option == "d":  # Depositar
            depositar(clientes)

        elif option == "s":  # Sacar
            sacar(clientes)

        elif option == "e":  # Extrato
            exibir_extrato(clientes)

        elif option == "q":  # QUIT
            print(MENSAGEM)
            break

        else:
            print("Operação inválida, por favor selecione novamente a opção desejada")


# Código Rodando
main()
