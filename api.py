from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3, bcrypt, jwt
from datetime import datetime, timedelta

SECRET_KEY = "minha_chave_super_secreta"
app = FastAPI()

# ==================== MODELOS ====================
class LoginRequest(BaseModel):
    cpf: str
    senha: str

class ClienteRequest(BaseModel):
    cpf: str
    nome: str
    data_nascimento: str
    endereco: str
    senha: str

class ContaRequest(BaseModel):
    cliente_cpf: str

class TransacaoRequest(BaseModel):
    tipo: str
    valor: float
    conta_numero: int
    destino_numero: int | None = None

# ==================== AUTENTICAÇÃO ====================
@app.post("/login")
def login(request: LoginRequest):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT senha FROM clientes WHERE cpf=?", (request.cpf,))
    cliente = cursor.fetchone()
    conexao.close()

    if cliente and bcrypt.checkpw(request.senha.encode("utf-8"), cliente[0]):
        payload = {"cpf": request.cpf, "exp": datetime.utcnow() + timedelta(minutes=30)}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="CPF ou senha inválido")

def validar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["cpf"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# ==================== CLIENTES ====================
@app.post("/clientes")
def criar_cliente(request: ClienteRequest):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    senha_hash = bcrypt.hashpw(request.senha.encode("utf-8"), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO clientes (cpf, nome, data_nascimento, endereco, senha) VALUES (?, ?, ?, ?, ?)",
                       (request.cpf, request.nome, request.data_nascimento, request.endereco, senha_hash))
        conexao.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    finally:
        conexao.close()
    return {"mensagem": "Cliente criado com sucesso!"}

@app.get("/clientes/{cpf}")
def obter_cliente(cpf: str):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT cpf, nome, data_nascimento, endereco FROM clientes WHERE cpf=?", (cpf,))
    cliente = cursor.fetchone()
    conexao.close()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"cpf": cliente[0], "nome": cliente[1], "data_nascimento": cliente[2], "endereco": cliente[3]}

@app.put("/clientes/{cpf}")
def atualizar_cliente(cpf: str, request: ClienteRequest):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE clientes SET nome=?, data_nascimento=?, endereco=? WHERE cpf=?",
                   (request.nome, request.data_nascimento, request.endereco, cpf))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Cliente atualizado com sucesso!"}


@app.delete("/clientes/{cpf}")
def excluir_cliente(cpf: str):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes WHERE cpf=?", (cpf,))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Cliente excluído com sucesso!"}


# ==================== CONTAS ====================
@app.post("/contas")
def criar_conta(request: ContaRequest):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes WHERE cpf=?", (request.cliente_cpf,))
    cliente = cursor.fetchone()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cursor.execute("INSERT INTO contas (agencia, saldo, cliente_cpf) VALUES (?, ?, ?)",
                   ("0001", 0.0, request.cliente_cpf))
    conexao.commit()

    numero = cursor.lastrowid  # pega o número gerado automaticamente
    conexao.close()
    return {"mensagem": "Conta criada com sucesso!", "numero": numero}


@app.get("/contas/{numero}")
def obter_conta(numero: int):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT numero, agencia, saldo, cliente_cpf FROM contas WHERE numero=?", (numero,))
    conta = cursor.fetchone()
    conexao.close()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"numero": conta[0], "agencia": conta[1], "saldo": conta[2], "cliente_cpf": conta[3]}

@app.get("/contas/por-cpf/{cpf}")
def obter_conta_por_cpf(cpf: str):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT c.numero, c.agencia, c.saldo, cl.nome
        FROM contas c
        JOIN clientes cl ON c.cliente_cpf = cl.cpf
        WHERE cl.cpf = ?
    """, (cpf,))
    conta = cursor.fetchone()
    conexao.close()

    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada para esse CPF")

    return {
        "numero": conta[0],
        "agencia": conta[1],
        "saldo": conta[2],
        "nome_cliente": conta[3]
    }   

@app.put("/contas/{numero}")
def atualizar_conta(numero: int, agencia: str):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE contas SET agencia=? WHERE numero=?", (agencia, numero))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Conta atualizada com sucesso!"}

@app.delete("/contas/{numero}")
def excluir_conta(numero: int):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT saldo FROM contas WHERE numero=?", (numero,))
    conta = cursor.fetchone()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    if conta[0] > 0:
        raise HTTPException(status_code=400, detail="Não é possível excluir conta com saldo positivo")

    cursor.execute("DELETE FROM contas WHERE numero=?", (numero,))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Conta excluída com sucesso!"}


# ==================== TRANSAÇÕES ====================
@app.post("/transacoes")
def registrar_transacao(request: TransacaoRequest):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    # verificar saldo para saque/transferência
    if request.tipo in ["Saque", "Transferência enviada"]:
        cursor.execute("""
            SELECT SUM(
                CASE 
                    WHEN tipo = 'Depósito' OR tipo = 'Transferência recebida' THEN valor
                    WHEN tipo = 'Saque' OR tipo = 'Transferência enviada' THEN -valor
                    ELSE 0 END
            )
            FROM transacoes WHERE conta_numero = ?
        """, (request.conta_numero,))
        saldo = cursor.fetchone()[0] or 0.0
        if request.valor > saldo:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

    data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    if request.tipo == "Transferência enviada":
        cursor.execute("INSERT INTO transacoes (tipo, valor, data, conta_numero) VALUES (?, ?, ?, ?)",
                       ("Transferência enviada", request.valor, data, request.conta_numero))
        cursor.execute("INSERT INTO transacoes (tipo, valor, data, conta_numero) VALUES (?, ?, ?, ?)",
                       ("Transferência recebida", request.valor, data, request.destino_numero))
    else:
        cursor.execute("INSERT INTO transacoes (tipo, valor, data, conta_numero) VALUES (?, ?, ?, ?)",
                       (request.tipo, request.valor, data, request.conta_numero))

    conexao.commit()
    conexao.close()
    return {"mensagem": "Transação registrada com sucesso!"}

@app.get("/extrato/{numero}")
def extrato(numero: int):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo, valor, data FROM transacoes WHERE conta_numero=? ORDER BY data", (numero,))
    transacoes = cursor.fetchall()
    conexao.close()

    saldo = 0
    extrato = []
    for tipo, valor, data in transacoes:
        if tipo in ("Depósito", "Transferência recebida"):
            saldo += valor
        elif tipo in ("Saque", "Transferência enviada"):
            saldo -= valor
        extrato.append({"tipo": tipo, "valor": valor, "data": data})

    return {"conta": numero, "saldo": saldo, "transacoes": extrato}
