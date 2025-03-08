from datetime import datetime

def depositar(saldo, extrato):
    try:
        valor = float(input("Informe o valor do depósito: ").replace(",", "."))  # Aceita "," como separador decimal
        if valor > 0:
            saldo += valor
            extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Depósito: R$ {valor:.2f}")
            print("\n✅ Depósito realizado com sucesso!\n")
        else:
            print("\n❌ Operação falhou! O valor informado é inválido.\n")
    except ValueError:
        print("\n❌ Entrada inválida! Digite um número válido.\n")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, LIMITE_SAQUES, limite):
    try:
        valor = float(input("Informe o valor do saque: ").replace(",", "."))
        
        if valor <= 0:
            print("\n❌ Operação falhou! O valor informado é inválido.\n")
        elif valor > saldo:
            print("\n❌ Operação falhou! Você não tem saldo suficiente.\n")
        elif valor > limite:
            print(f"\n❌ Operação falhou! O saque máximo permitido por operação é de R$ {limite:.2f}.\n")
        elif numero_saques >= LIMITE_SAQUES:
            print("\n❌ Operação falhou! Número máximo de saques excedido.\n")
        else:
            saldo -= valor
            extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Saque: R$ {valor:.2f}")
            numero_saques += 1
            print("\n✅ Saque realizado com sucesso!\n")
    
    except ValueError:
        print("\n❌ Entrada inválida! Digite um número válido.\n")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================\n")
    if not extrato:
        print("Nenhuma movimentação registrada.\n")
    else:
        for item in extrato:
            print(item)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("==========================================\n")

def main():
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3

    menu = """
    🔹 Escolha uma opção:

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    print("\n💰 Bem-vindo ao sistema bancário! 💰\n")

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, LIMITE_SAQUES, limite)
        elif opcao == "e":
            exibir_extrato(saldo, extrato)
        elif opcao == "q":
            print("\nObrigado por usar nosso sistema bancário. Até mais! 👋\n")
            break
        else:
            print("\n❌ Operação inválida! Tente novamente.\n")

if __name__ == "__main__":
    main()


