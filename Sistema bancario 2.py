import colorama
from colorama import Fore

def menu():
    menu = """
    [MENU]
    |
    |\t[1] Depositar
    |\t[2] Sacar
    |\t[3] Extrato
    |\t[4] Novo usuário 
    |\t[5] Nova conta
    |\t[6] Listar contas
    |\t[7] Sair
    |
    [MENU]

    =>  """
    return int(input(menu))

def criar_usuario(usuarios):
    cpf = input("Informe o CPF(somente números): ")
    usuario = filtrar_usuario(cpf,usuarios)
    if usuario:
        print(Fore.RED + "Já existe um usuário com esse CPF!"+ Fore.RESET)
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aa): ")
    endereco = input("Informe o endereço (logradouro, num - bairro - cidade/sigla estado): ")

    usuarios.append({"nome":nome,
                     "data_nascimento":data_nascimento,
                     "cpf":cpf,
                     "endereco":endereco
                     })
    print(Fore.GREEN+"Usuário criado com sucesso!"+Fore.RESET)

def filtrar_usuario(cpf,usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def filtrar_conta(contas,conta_inserida):
    filtrar_conta = [conta for conta in contas if conta["numero_conta"] == conta_inserida]
    return filtrar_conta[0] if filtrar_conta else None

def criar_conta(agencia,numero_conta,usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print(Fore.GREEN + "Conta criada com sucesso!" + Fore.RESET)
        return {"agencia":agencia, "numero_conta":numero_conta, "usuario": usuario, "saldo_conta":0, "cpf":cpf, "extrato":"","num_saques":0}
    print(Fore.RED + "Usuário não encontrado, fluxo de criação de conta encerrado!" + Fore.RESET)

def depositar(val,contas,usuarios, /): # por posição
    cpf = input("Informe o CPF(somente números): ")
    usuario = filtrar_usuario(cpf,usuarios)
    if usuario:
        if val > 0:
            [print("Disponivel conta: ",conta["numero_conta"]) for conta in contas if conta["cpf"]==cpf]
            conta_inserida = int(input("Insira a conta de sua escolha: "))
            m = filtrar_conta(contas,conta_inserida)
            if not m:
                print(Fore.RED + "\nErro! Não foi possivel realizar o deposito, a conta não era válido." + Fore.RESET)
                return 

            m["saldo_conta"] = m["saldo_conta"] + val 
            m["extrato"] += f"\n\t[1] Depósito: R$ {val:.2f}"  
            print(Fore.GREEN + "Depósito realizado com sucesso!" + Fore.RESET)
        else:
            print(Fore.RED + "\nErro! Não foi possivel realizar o deposito pois o valor não era válido." + Fore.RESET)
    else:
        print(Fore.RED + "\nErro! Não foi possivel realizar o deposito pois o usuário não foi encontrado." + Fore.RESET)

def sacar(*, val,NUM_LIM_SAQUE,limite_sacar,usuarios,contas):
    cpf = input("Informe o CPF(somente números): ")
    usuario = filtrar_usuario(cpf,usuarios)

    if usuario:
        [print("Disponivel conta: ",conta["numero_conta"]) for conta in contas if conta["cpf"]==cpf]
        conta_inserida = int(input("Insira a conta de sua escolha: "))
        m = filtrar_conta(contas,conta_inserida)
        if not m:
                print(Fore.RED + "\nErro! Não foi possivel realizar o deposito, a conta não era válido." + Fore.RESET)
                return 
        if val > m["saldo_conta"]:
            print(Fore.RED + "\nErro! Não foi possivel realizar o saque pois o saldo não é suficiente." + Fore.RESET)
        elif val > limite_sacar:
            print(Fore.RED + "\nErro! Não foi possivel realizar o saque pois o saque excedeu o valor limite." + Fore.RESET)
        elif m["num_saques"] >= NUM_LIM_SAQUE:
            print(Fore.RED + "\nErro! Não foi possivel realizar o saque pois foi excedido o número máximo de saques." + Fore.RESET)
        elif val > 0:
            m["saldo_conta"] = m["saldo_conta"] - val
            m["extrato"] += f"\n\t[2] Saque: R$ {val:.2f}"
            m["num_saques"]+=1
            print(Fore.GREEN + "Saque realizado com sucesso!" + Fore.RESET)
        else:
            print(Fore.RED + "\nErro! O valor informado não é válido." + Fore.RESET)
    else:
        print(Fore.RED + "\nErro! O usuário não foi encontrado." + Fore.RESET)

def imprimirExtrato(usuarios,/,*,contas): 
    cpf = input("Informe o CPF(somente números): ")
    usuario = filtrar_usuario(cpf,usuarios)
    if usuario:
        [print("Disponivel conta: ",conta["numero_conta"]) for conta in contas if conta["cpf"]==cpf]
        conta_inserida = int(input("Insira a conta de sua escolha: "))
        m = filtrar_conta(contas,conta_inserida)
        if not m:
            print(Fore.RED + "\nErro! A conta não era válido." + Fore.RESET)
            return 
        print('\n')
        print(Fore.BLUE + f" EXTRATO {conta_inserida} ".center(40,"="))
        print(f"\nNão houve movimentação na conta.\n" if not m["extrato"] else m["extrato"])
        print(f"\n\tSaldo: R$ {m['saldo_conta']:.2f}\n"+("="*40) + Fore.RESET)
    else:
        print(Fore.RED + "\nErro! O CPF não era válido." + Fore.RESET)

def listar_contas(contas):
    for conta in contas:
        linha = f"""\n
{("-"*50)}
    Agência:\t{conta['agencia']}
    C/C:\t{conta['numero_conta']}
    Titular:\t{conta['usuario']['nome']}
    CPF:\t{conta["cpf"]}
    Saldo:\t{conta['saldo_conta']}
{("-"*50)}
        """
        print(Fore.BLUE+linha+Fore.RESET)

def main():

    NUM_LIM_SAQUE = 3
    AGENCIA = "0001"
    limite_sacar = 500
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 1: 
            val = float(input("Inserir o valor do depósito: "))
            depositar(val,contas,usuarios)

        elif opcao == 2:
            val = float(input("Inserir o valor do saque: "))
            sacar(
                contas = contas,
                usuarios = usuarios,
                val = val,
                NUM_LIM_SAQUE = NUM_LIM_SAQUE,
                limite_sacar = limite_sacar
                )
        
        elif opcao == 3:
            imprimirExtrato(usuarios,contas=contas)
        
        elif opcao == 4:
            criar_usuario(usuarios)
        
        elif opcao == 5:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA,numero_conta,usuarios)
            if conta:
                contas.append(conta)
        
        elif opcao == 6:
            listar_contas(contas)
        
        elif opcao == 7:
            break
        
        else:
            print(Fore.RED + "\n!!! Opção inserida é inválida. Selecione novamente." + Fore.RESET)

main()
    
