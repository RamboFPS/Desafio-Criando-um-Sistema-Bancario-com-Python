import sqlite3
import bcrypt

# Conectar ao banco
conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

# Buscar todos os clientes e suas senhas atuais
cursor.execute("SELECT cpf, senha FROM clientes")
clientes = cursor.fetchall()

for cpf, senha in clientes:
    # Se a senha ainda está em texto puro (str)
    if isinstance(senha, str):
        print(f"Convertendo senha do cliente {cpf}...")

        # Gerar hash bcrypt
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

        # Atualizar no banco como BLOB
        cursor.execute("UPDATE clientes SET senha=? WHERE cpf=?", (sqlite3.Binary(senha_hash), cpf))

conexao.commit()
conexao.close()

print("✅ Todas as senhas foram convertidas para bcrypt (BLOB) com sucesso!")
