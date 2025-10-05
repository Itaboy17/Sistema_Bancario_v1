# Sistema bancário versão 2

# Funções
def menu():
    menu = '''    
    ============ MENU ============
            Bamko Manikômico

        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        [nc] Nova Conta
        [lc] Listar Contas
        [nu] Novo Usuário

    ==============================
    => '''
    return input(menu)


def depositar(saldo, extrato, qntd_depo):
    LIM_TENTA_DEPO = 3

    tentativas_dep = -1
    valor = float(input("Insira um valor para depósito: R$"))

    while valor <= 0 and tentativas_dep < LIM_TENTA_DEPO:
        tentativas_dep += 1
        print(
            f"Você possui mais {LIM_TENTA_DEPO - tentativas_dep} tentativas. ")
        valor = float(input("Insira um valor para depósito: R$"))

    if valor > 0:
        saldo += valor
        qntd_depo += 1
        extrato += f"Depósito {qntd_depo}: R${valor:.2f}\n"
        print(f"Depósito realizado com sucesso.")
        print(f"Seu saldo agora é: R${saldo:.2f}\n")

    return saldo, extrato, qntd_depo


def sacar(*, saldo, extrato, qntd_saq, qntd_saq_dia):
    LIM_TENTA_SAQ = 3
    LIM_SAQ_DIA = 3
    LIM_VALOR_SAQ = 500

    tentativas_saq = 1
    pode_sacar = qntd_saq_dia < LIM_SAQ_DIA

    if pode_sacar:
        valor = float(input("Insira um valor para sacar: R$"))
        valor_valido = valor <= saldo and valor > 0
        excedeu_tentativas = tentativas_saq >= LIM_TENTA_SAQ

        while not valor_valido and not excedeu_tentativas:
            tentativas_saq += 1
            print(
                f"Você possui mais {LIM_TENTA_SAQ - tentativas_saq + 1} tentativas.")
            valor = float(input("Insira um valor para sacar: R$"))

            excedeu_tentativas = tentativas_saq >= LIM_TENTA_SAQ
            valor_valido = valor < saldo and valor > 0

        if valor_valido:
            saldo -= valor
            qntd_saq_dia += 1
            qntd_saq += 1
            extrato += f"Saque {qntd_saq}: R${valor:.2f}\n"
            print(f"\nSaque realizado com sucesso!\n")
            print(f"Seu saldo agora é: R${saldo:.2f}\n")

        elif not valor_valido:
            print(
                "\n============================================================================================")
            print(
                f"Você não possui limite para sacar ou o valor é inválido. Repita a transação corretamente.")
            print(
                "============================================================================================")

    else:
        print("Você não pode mais sacar hoje. Tente novamente amanhã!")

    return saldo, extrato, qntd_saq, qntd_saq_dia


def exibir_extrato(saldo, /, *, extrato):
    print("============== EXTRATO ==============\n")

    if not extrato:
        print("Não houve transações nessa conta.")

    else:
        print(extrato)
        print(f"\nSaldo: R${saldo:.2f}")
        print("=====================================")


def filtrar_usuario(cpf, usuarios):
    filtro = [usuario for usuario in usuarios if usuario["cpf"] == cpf]

    return filtro[0] if filtro else None


def novo_usuario(usuarios):
    # nome, nascimento, cpf, endereço
    cpf = input("Insira seu CPF (somente números): ")
    filtro = filtrar_usuario(cpf, usuarios)

    if filtro:
        print("\nCPF já cadastrado para outro usuário. Insira um CPF novo.\n")

    nome = input("\nInsira seu nome completo: ")
    data_nasc = input("\nInsira sua data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "\nInsira seu endereço (rua, num - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nasc": data_nasc,
                    "cpf": cpf, "endereco": endereco})

    print("\n== Usuário criado com sucesso! ==")

    return usuarios


def criar_conta(AGENCIA, num_conta, usuarios):
    cpf = input("Insira seu CPF (somente números): ")
    print(cpf)
    usuario = filtrar_usuario(cpf, usuarios)
    print(usuario)

    if usuario != None:
        conta = {"agencia": AGENCIA, "num_conta": num_conta, "usuario": usuario}
        
        print("Conta Criada com sucesso!")
        print("=================================\n")
        
        print("\n==================================")
        

        return conta

    print("\nUsuário não encontrado. Crie um usuário primeiro para adicionar uma conta.")

def listar_contas(contas):
    for conta in contas:
        conta_info = f"""
        Agência: {conta['agencia']}
        Número da Conta Corrente: {conta['num_conta']}
        Titular da Conta: {conta['usuario']['nome']}
        CPF do Titular da Conta: {conta['usuario']['cpf']}
        """
        print(conta_info)

def main():
    # Variáveis
    saldo = 10000.00
    valor = 0.00
    qntd_saq = 0
    qntd_depo = 0
    qntd_saq_dia = 0
    transacoes_dia = 0
    extrato = ""
    usuarios = [{"nome": "Samuel", "data_nasc": "30-12-2003", "cpf": "07032795307",
                 "endereco": "Rua Dom Lino, 188 - Parquelândia - Fortaleza/CE"}]
    contas = []

    # Constantes
    MENSAGEM = "\nEH U MANIKAS HEHE"
    AGENCIA = "0001"

    # Estrutura Principal do Sistema
    while True:
        option = menu()
        transacoes = qntd_depo + qntd_saq

        if option == "d":  # DEPÓSITO
            saldo, extrato, qntd_depo = depositar(saldo, extrato, qntd_depo)

        elif option == "s":  # SAQUE
            saldo, extrato, qntd_saq, qntd_saq_dia = sacar(
                saldo=saldo, extrato=extrato, qntd_saq=qntd_saq, qntd_saq_dia=qntd_saq_dia)

        elif option == "e": #Extrato
            saldo, extrato = exibir_extrato(saldo, extrato=extrato)

        elif option == "nc": #nova conta
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)
            
        elif option == "lc": #listar contas
            listar_contas(contas)

        elif option == "nu": #novo usuário
            usuarios = novo_usuario(usuarios)

        elif option == "q":  # QUIT
            print(MENSAGEM)
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a opção desejada")


# Código Rodando
main()
