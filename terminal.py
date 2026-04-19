import sqlite3
import textwrap
import datetime
import jwt
import bcrypt

# Conexão com SQLite
SECRET_KEY = "minha_chave_super_secreta"

def login():
    cpf = input("CPF: ")
    senha = input("Senha: ")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT senha FROM clientes WHERE cpf=?", (cpf,))
    cliente = cursor.fetchone()
    conexao.close()

    if cliente and bcrypt.checkpw(senha.encode("utf-8"), cliente[0]):
        payload = {
            "cpf": cpf,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        print("\n✅ Login realizado com sucesso!")
        return token
    else:
        print("\n⚠️ CPF ou senha inválidos!")
        return None



def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["cpf"]
    except jwt.ExpiredSignatureError:
        print("⚠️ Token expirado!")
    except jwt.InvalidTokenError:
        print("⚠️ Token inválido!")
    return None
conexao = sqlite3.connect("banco.db", timeout=10)
cursor = conexao.cursor()

# ==================== FUNÇÕES DE BANCO ====================

def salvar_cliente():
    cpf = input("CPF: ")
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço: ")
    senha = input("Senha: ")

    # gera hash da senha
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

    cliente = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "senha": senha_hash
    }

    cursor.execute("""
        INSERT INTO clientes (cpf, nome, data_nascimento, endereco, senha)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente["cpf"], cliente["nome"], cliente["data_nascimento"], cliente["endereco"], cliente["senha"]))
    conexao.commit()

    print("\n=== Cliente criado com sucesso! ===")

def salvar_conta(conta):
    cursor.execute("""
        INSERT INTO contas (numero, agencia, saldo, cliente_cpf)
        VALUES (?, ?, ?, ?)
    """, (conta["numero"], conta["agencia"], conta["saldo"], conta["cliente_cpf"]))
    conexao.commit()

def salvar_transacao(tipo, valor, conta_numero):
    try:
        cursor.execute("""
            INSERT INTO transacoes (tipo, valor, data, conta_numero)
            VALUES (?, ?, ?, ?)
        """, (tipo, valor, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), conta_numero))
        conexao.commit()
        print("\n✅ Transação registrada com sucesso!")
    except sqlite3.IntegrityError:
        print("\n⚠️ Transação duplicada detectada. Operação cancelada.")


def registrar_transacao(tipo, valor, data, conta_numero):
    try:
        with sqlite3.connect("banco.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO transacoes (tipo, valor, data, conta_numero)
                VALUES (?, ?, ?, ?)
            """, (tipo, valor, data, conta_numero))
            conexao.commit()
            print("✅ Transação registrada com sucesso!")
    except sqlite3.IntegrityError as e:
        print("⚠️ Transação duplicada detectada. Operação cancelada.")
        print("Detalhes:", e)
  

def carregar_clientes():
    cursor.execute("SELECT * FROM clientes")
    return cursor.fetchall()

def carregar_contas():
    cursor.execute("SELECT * FROM contas")
    return cursor.fetchall()

def carregar_transacoes(conta_numero):
    cursor.execute("SELECT tipo, valor, data FROM transacoes WHERE conta_numero=?", (conta_numero,))
    return cursor.fetchall()

# ==================== INTERFACE ====================

def menu():
    opcoes = """\n
    ================ MENU ================
    [nu]\tNovo cliente
    [nc]\tNova conta
    [d]\tDepositar
    [s]\tSacar
    [t]\tTransferir
    [e]\tExtrato
    [q]\tSair
    => """
    return input(textwrap.dedent(opcoes))

def criar_cliente():
    cpf = input("CPF: ")
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço: ")
    cliente = {"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco}
    salvar_cliente(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta():
    cpf = input("CPF do cliente: ")
    cursor.execute("SELECT * FROM clientes WHERE cpf=?", (cpf,))
    cliente = cursor.fetchone()
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero = len(carregar_contas()) + 1
    conta = {"numero": numero, "agencia": "0001", "saldo": 0.0, "cliente_cpf": cpf}
    salvar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")

def depositar():
    numero = int(input("Número da conta: "))
    valor = float(input("Valor do depósito: "))
    salvar_transacao("Depósito", valor, numero)
    print("\n=== Depósito realizado com sucesso! ===")

def sacar():
    numero = int(input("Número da conta: "))
    valor = float(input("Valor do saque: "))

    # calcular saldo atual pelas transações
    cursor.execute("""
        SELECT SUM(
            CASE 
                WHEN tipo = 'Depósito' OR tipo = 'Transferência recebida' THEN valor
                WHEN tipo = 'Saque' OR tipo = 'Transferência enviada' THEN -valor
                ELSE 0 END
        )
        FROM transacoes
        WHERE conta_numero = ?
    """, (numero,))
    saldo = cursor.fetchone()[0] or 0.0

    if valor > saldo:
        print("\n@@@ Saldo insuficiente! @@@")
        return

    salvar_transacao("Saque", valor, numero)
    print("\n=== Saque realizado com sucesso! ===")

def transferir():
    origem = int(input("Conta origem: "))
    destino = int(input("Conta destino: "))
    valor = float(input("Valor da transferência: "))

    # calcular saldo da origem
    cursor.execute("""
        SELECT SUM(
            CASE 
                WHEN tipo = 'Depósito' OR tipo = 'Transferência recebida' THEN valor
                WHEN tipo = 'Saque' OR tipo = 'Transferência enviada' THEN -valor
                ELSE 0 END
        )
        FROM transacoes
        WHERE conta_numero = ?
    """, (origem,))
    saldo_origem = cursor.fetchone()[0] or 0.0

    if valor > saldo_origem:
        print("\n@@@ Saldo insuficiente! @@@")
        return

    salvar_transacao("Transferência enviada", valor, origem)
    salvar_transacao("Transferência recebida", valor, destino)
    print("\n=== Transferência realizada com sucesso! ===")

def extrato():
    numero = int(input("Número da conta: "))
    
    cursor.execute("""
        SELECT cli.nome 
        FROM contas c
        JOIN clientes cli ON c.cliente_cpf = cli.cpf
        WHERE c.numero = ?
    """, (numero,))
    cliente = cursor.fetchone()
    if not cliente:
        print("\n@@@ Conta não encontrada! @@@")
        return
    
    cliente_nome = cliente[0]

    cursor.execute("""
        SELECT tipo, valor, data
        FROM transacoes
        WHERE conta_numero = ?
        ORDER BY data
    """, (numero,))
    transacoes = cursor.fetchall()

    print(f"\n================ EXTRATO DE {cliente_nome} ================")
    saldo = 0
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for tipo, valor, data in transacoes:
            if tipo in ("Depósito", "Transferência recebida"):
                saldo += valor
            elif tipo in ("Saque", "Transferência enviada"):
                saldo -= valor
            print(f"{tipo} em {data} - R$ {valor:.2f}")
    print(f"\nSaldo atual calculado: R$ {saldo:.2f}")
    print("===========================================================")


# ==================== MAIN ====================

def main():
    token = None
    while not token:
        token = login()

    while True:
        cpf = validar_token(token)
        if not cpf:
            print("\n⚠️ Você precisa fazer login novamente.")
            token = login()
            continue
        opcao = menu()
        if opcao == "nu":
            criar_cliente()
        elif opcao == "nc":
            criar_conta()
        elif opcao == "d":
            depositar()
        elif opcao == "s":
            sacar()
        elif opcao == "t":
            transferir()
        elif opcao == "e":
            extrato()
        elif opcao == "q":
            break
        else:
            print("\n@@@ Opção inválida! @@@")

if __name__ == "__main__":
    main()
