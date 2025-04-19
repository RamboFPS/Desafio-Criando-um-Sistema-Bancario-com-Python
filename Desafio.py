from datetime import datetime

def cadastrar_usuario(usuarios):
    print("\n📋 Cadastro de Usuário")
    nome = input("Digite o nome completo: ").strip()
    cpf = input("Digite o CPF (somente números): ").strip()

    # Validação: CPF é obrigatório
    if not cpf:
        print("\n❌ Operação falhou! CPF é obrigatório.\n")
        return usuarios

    data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Digite o endereço (Ex.: Rua, nº - Bairro - Cidade/Estado): ").strip()
    
    # Verifica se o CPF já está cadastrado
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("\n❌ Operação falhou! CPF já cadastrado.\n")
            return usuarios
    
    # Adiciona o novo usuário à lista
    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })
    print("\n✅ Usuário cadastrado com sucesso!\n")
    return usuarios

def cadastrar_conta_bancaria(usuarios, contas, LIMITE_CONTAS_POR_USUARIO):
    print("\n📋 Cadastro de Conta Bancária")
    cpf = input("Digite o CPF do usuário: ").strip()
    
    # Verifica se o usuário existe
    usuario = None
    for u in usuarios:
        if u["cpf"] == cpf:
            usuario = u
            break
    
    if not usuario:
        print("\n❌ Operação falhou! Usuário não encontrado.\n")
        return contas
    
    # Verifica o número de contas que o usuário já possui
    contas_existentes = [conta for conta in contas if conta["cpf"] == cpf]
    if len(contas_existentes) >= LIMITE_CONTAS_POR_USUARIO:
        print("\n❌ Operação falhou! Limite de contas por usuário atingido.\n")
        return contas
    
    # Escolhe o tipo de conta
    tipo_conta = input("Escolha o tipo de conta [1] Pessoa Física [2] Pessoa Jurídica: ").strip()
    if tipo_conta == "1":
        tipo_conta = "Pessoa Física"
    elif tipo_conta == "2":
        tipo_conta = "Pessoa Jurídica"
    else:
        print("\n❌ Operação falhou! Tipo de conta inválido.\n")
        return contas
    
    # Verifica se o usuário já tem uma conta do mesmo tipo
    for conta in contas_existentes:
        if conta["tipo_conta"] == tipo_conta:
            print("\n❌ Operação falhou! O usuário já possui uma conta deste tipo.\n")
            return contas
    
    # Gera o número da conta com sequência iniciando de 0001
    numero_conta = f"{len(contas) + 1:04}"  # Gera número no formato 0001, 0002, etc.
    contas.append({
        "numero_conta": numero_conta,
        "cpf": cpf,
        "tipo_conta": tipo_conta,
        "saldo": 0,
        "extrato": []
    })
    print(f"\n✅ Conta cadastrada com sucesso! Número da conta: {numero_conta}, Tipo: {tipo_conta}\n")
    return contas

def excluir_usuario(usuarios, contas):
    cpf = input("Digite o CPF do usuário a ser excluído: ").strip()
    
    # Verifica se o usuário existe
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        print("\n❌ Operação falhou! Usuário não encontrado.\n")
        return usuarios, contas
    
    # Remove o usuário e suas contas associadas
    usuarios = [u for u in usuarios if u["cpf"] != cpf]
    contas = [c for c in contas if c["cpf"] != cpf]
    print("\n✅ Usuário e suas contas foram excluídos com sucesso!\n")
    return usuarios, contas

def encerrar_conta_bancaria(contas):
    numero_conta = input("Digite o número da conta a ser encerrada: ").strip()
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)

    if not conta:
        print("\n❌ Operação falhou! Conta não encontrada.\n")
        return contas

    if conta["saldo"] > 0:
        print("\n❌ Operação falhou! Não é possível encerrar a conta enquanto houver saldo.\n")
        return contas

    contas = [c for c in contas if c["numero_conta"] != numero_conta]
    print("\n✅ Conta encerrada com sucesso!\n")
    return contas

def consultar_contas(contas, usuarios):
    print("\n================ CONTAS CADASTRADAS ================\n")
    if not contas:
        print("Nenhuma conta cadastrada.\n")
    else:
        for conta in contas:
            # Obtém o nome do usuário vinculado ao CPF da conta
            usuario = next((u for u in usuarios if u["cpf"] == conta["cpf"]), None)
            nome_usuario = usuario["nome"] if usuario else "Usuário não encontrado"
            print(f"Conta: {conta['numero_conta']} | CPF: {conta['cpf']} | Titular: {nome_usuario} | Tipo: {conta['tipo_conta']}")
    print("===================================================\n")


def realizar_deposito(contas):
    numero_conta = input("Digite o número da conta: ").strip()
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)
    if not conta:
        print("\n❌ Operação falhou! Conta não encontrada.\n")
        return
    try:
        valor = float(input("Informe o valor do depósito: ").replace(",", "."))
        if valor > 0:
            conta["saldo"] += valor
            conta["extrato"].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Depósito: R$ {valor:.2f}")
            print("\n✅ Depósito realizado com sucesso!\n")
        else:
            print("\n❌ Operação falhou! O valor informado é inválido.\n")
    except ValueError:
        print("\n❌ Entrada inválida! Digite um número válido.\n")

def realizar_saque(contas, limite):
    numero_conta = input("Digite o número da conta: ").strip()
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)
    if not conta:
        print("\n❌ Operação falhou! Conta não encontrada.\n")
        return
    try:
        valor = float(input("Informe o valor do saque: ").replace(",", "."))
        if valor <= 0:
            print("\n❌ Operação falhou! O valor informado é inválido.\n")
        elif valor > conta["saldo"]:
            print("\n❌ Operação falhou! Saldo insuficiente.\n")
        elif valor > limite:
            print(f"\n❌ Operação falhou! O saque máximo permitido é de R$ {limite:.2f}.\n")
        else:
            conta["saldo"] -= valor
            conta["extrato"].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Saque: R$ {valor:.2f}")
            print("\n✅ Saque realizado com sucesso!\n")
    except ValueError:
        print("\n❌ Entrada inválida! Digite um número válido.\n")

def realizar_transferencia(contas):
    numero_conta_origem = input("Digite o número da conta de origem: ").strip()
    conta_origem = next((c for c in contas if c["numero_conta"] == numero_conta_origem), None)
    if not conta_origem:
        print("\n❌ Operação falhou! Conta de origem não encontrada.\n")
        return
    
    numero_conta_destino = input("Digite o número da conta de destino: ").strip()
    conta_destino = next((c for c in contas if c["numero_conta"] == numero_conta_destino), None)
    if not conta_destino:
        print("\n❌ Operação falhou! Conta de destino não encontrada.\n")
        return
    
    # Verifica se as contas de origem e destino são iguais
    if numero_conta_origem == numero_conta_destino:
        print("\n❌ Operação falhou! A conta de destino não pode ser a mesma que a conta de origem.\n")
        return
    
    try:
        valor = float(input("Informe o valor da transferência: ").replace(",", "."))
        if valor <= 0:
            print("\n❌ Operação falhou! O valor informado é inválido.\n")
        elif valor > conta_origem["saldo"]:
            print("\n❌ Operação falhou! Saldo insuficiente na conta de origem.\n")
        else:
            conta_origem["saldo"] -= valor
            conta_destino["saldo"] += valor
            conta_origem["extrato"].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Transferência enviada: R$ {valor:.2f} para conta {numero_conta_destino}")
            conta_destino["extrato"].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - Transferência recebida: R$ {valor:.2f} da conta {numero_conta_origem}")
            print("\n✅ Transferência realizada com sucesso!\n")
    except ValueError:
        print("\n❌ Entrada inválida! Digite um número válido.\n")

def exibir_extrato(contas, usuarios):
    numero_conta = input("Digite o número da conta: ").strip()
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)
    if not conta:
        print("\n❌ Operação falhou! Conta não encontrada.\n")
        return
    
    # Obtém o nome do usuário vinculado ao CPF da conta
    usuario = next((u for u in usuarios if u["cpf"] == conta["cpf"]), None)
    nome_usuario = usuario["nome"] if usuario else "Usuário não encontrado"

    # Exibe informações da conta
    print("\n================ EXTRATO ================\n")
    print(f"Conta: {conta['numero_conta']} | CPF: {conta['cpf']} | Titular: {nome_usuario} | Tipo: {conta['tipo_conta']}")
    print("------------------------------------------\n")
    
    if not conta["extrato"]:
        print("Nenhuma movimentação registrada.\n")
    else:
        for item in conta["extrato"]:
            print(item)
    print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
    print("==========================================\n")

def encerrar_conta_bancaria(contas):
    numero_conta = input("Digite o número da conta a ser encerrada: ").strip()
    conta = next((c for c in contas if c["numero_conta"] == numero_conta), None)

    if not conta:
        print("\n❌ Operação falhou! Conta não encontrada.\n")
        return contas

    if conta["saldo"] > 0:
        print("\n❌ Operação falhou! Não é possível encerrar a conta enquanto houver saldo.\n")
        return contas

    contas = [c for c in contas if c["numero_conta"] != numero_conta]
    print("\n✅ Conta encerrada com sucesso!\n")
    return contas

def menu_cadastro(usuarios, contas, LIMITE_CONTAS_POR_USUARIO):
    while True:
        menu = """
        🔹 Menu de Cadastro:
        
        [1] Cadastrar Usuário
        [2] Cadastrar Conta Bancária
        [3] Listar Contas
        [4] Encerrar Conta Bancária
        [0] Voltar ao Menu Principal

        => """
        opcao = input(menu).strip()
        if opcao == "1":
            cadastrar_usuario(usuarios)
        elif opcao == "2":
            cadastrar_conta_bancaria(usuarios, contas, LIMITE_CONTAS_POR_USUARIO)
        elif opcao == "3":
            consultar_contas(contas, usuarios)
        elif opcao == "4":
            contas = encerrar_conta_bancaria(contas)
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida! Tente novamente.\n")

def main():
    usuarios = []  # Lista de usuários cadastrados
    contas = []  # Lista de contas bancárias cadastradas
    LIMITE_CONTAS_POR_USUARIO = 2  # Limite de contas por usuário
    limite_saque = 500  # Limite máximo de saque por operação


    menu_principal = """
    🔹 Menu Principal:
    
    [1] Depósito
    [2] Saque
    [3] Transferência
    [4] Extrato
    [5] Menu de Cadastro
    [0] Sair

    => """

    print("\n💰 Bem-vindo ao sistema bancário! 💰\n")

    while True:
        opcao = input(menu_principal).strip()
        if opcao == "1":
            realizar_deposito(contas)
        elif opcao == "2":
            realizar_saque(contas, limite_saque)
        elif opcao == "3":
            realizar_transferencia(contas)
        elif opcao == "4":
            exibir_extrato(contas, usuarios)
        elif opcao == "5":
            menu_cadastro(usuarios, contas, LIMITE_CONTAS_POR_USUARIO)
        elif opcao == "0":
            print("\nObrigado por usar nosso sistema bancário. Até mais! 👋\n")
            break
        else:
            print("\n❌ Opção inválida! Tente novamente.\n")

if __name__ == "__main__":
    main()