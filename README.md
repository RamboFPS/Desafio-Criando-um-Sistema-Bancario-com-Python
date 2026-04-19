💰 Sistema Bancário em Python com FastAPI
Este projeto implementa uma API REST que simula um sistema bancário simples, com funcionalidades como cadastro de clientes e contas, movimentações financeiras (depósitos, saques, transferências), emissão de extratos e autenticação segura. O sistema utiliza SQLite como banco de dados e está totalmente funcional.

📜 Funcionalidades
Cadastro de clientes com senha criptografada (bcrypt)

Criação e gerenciamento de contas bancárias

Login seguro com geração de token JWT válido por 30 minutos

Depósitos

Saques (com verificação de saldo)

Transferências entre contas

Emissão de extrato detalhado

Exclusão de clientes e contas

🔒 Segurança
Senhas armazenadas com bcrypt (hash seguro, não reversível)

Autenticação com JWT:

Cada login gera um token válido por 30 minutos

Operações financeiras só são permitidas com token válido

Tokens inválidos ou expirados exigem novo login

▶️ Como Usar
Clone este repositório

bash
git clone https://github.com/RamboFPS/Desafio-Criando-um-Sistema-Bancario-com-Python.git
Instale as dependências

bash
pip install fastapi uvicorn bcrypt PyJWT
Execute o servidor

bash
uvicorn api:app --reload
Acesse a documentação interativa (Swagger UI)

Código
http://127.0.0.1:8000/docs

Estrutura final da sua API
Clientes (CRUD completo)

POST /clientes → criar cliente

GET /clientes/{cpf} → consultar cliente

PUT /clientes/{cpf} → atualizar dados do cliente

DELETE /clientes/{cpf} → excluir cliente e contas associadas

Contas (CRUD completo com regras)

POST /contas → criar conta

GET /contas/{numero} → consultar conta

PUT /contas/{numero} → atualizar agência ou encerrar conta

DELETE /contas/{numero} → excluir conta (somente se saldo = 0)

## Transações (somente Create + Read)

POST /transacoes → registrar depósito, saque ou transferência

GET /extrato/{numero} → consultar extrato e saldo atualizado

🔒 Sem Update/Delete → transações são imutáveis, garantindo histórico confiável

✅ Benefícios dessa decisão
Auditoria: cada movimentação fica registrada permanentemente.

Segurança: evita manipulação indevida de histórico financeiro.

Consistência: saldo é sempre calculado a partir das transações registradas.

Aderência ao mundo real: bancos não permitem apagar ou editar movimentações já realizadas.

🛠️ Tecnologias Utilizadas
Python 3

FastAPI (framework web)

SQLite3 (banco de dados relacional)

bcrypt (hash de senhas)

PyJWT (JSON Web Token)