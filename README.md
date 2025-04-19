 # 💰 Sistema Bancário em Python

Este é um projeto de terminal que simula um sistema bancário simples, com funcionalidades como cadastro de usuários e contas, movimentações financeiras (depósitos, saques, transferências), geração de extratos, entre outros.

# 📜 Funcionalidades

Cadastro de usuários
Cadastro e gerenciamento de contas bancárias
Depósitos
Saques (com limite)
Transferências entre contas
Emissão de extrato
Exclusão de usuários e contas


# ▶️ Como Usar
Execute o script em um ambiente Python 3:
Ao iniciar, o sistema apresenta um menu principal, com as seguintes opções:

🔹 Menu Principal:

[1] Depósito
[2] Saque
[3] Transferência
[4] Extrato
[5] Menu de Cadastro
[0] Sair

# 🧩 Estrutura do Código
Função principal que inicializa o sistema, exibe o menu e coordena a execução das ações.

Menu específico para o gerenciamento de usuários e contas bancárias:

🔹 Menu de Cadastro:

[1] Cadastrar Usuário  
[2] Cadastrar Conta Bancária  
[3] Listar Contas  
[4] Encerrar Conta Bancária  
[0] Voltar ao Menu Principal

# 📦 Funções
## Usuários

Cadastra um novo usuário se o CPF for único
Exclui o usuário e todas as contas associadas ao CPF.
Contas Bancárias
Cria uma conta para um usuário existente, respeitando o limite e tipo da conta.
Lista todas as contas cadastradas com seus respectivos titulares.
Encerra uma conta se não houver saldo.

# Operações Financeiras
Realiza depósito em uma conta válida.
Realiza saque com verificação de saldo e limite por operação.
Realiza transferência entre contas diferentes.
Exibe o extrato e o saldo atual da conta.

# ⚙️ Regras de Negócio
Cada CPF pode ter no máximo 2 contas bancárias.

Um usuário não pode ter duas contas do mesmo tipo.
O valor máximo por saque é de R$ 500,00.
Não é possível encerrar contas com saldo positivo.
É necessário que os CPFs sejam únicos no sistema.
---

## 🎮 **Como Executar o Programa**
### 🔹 **1. Clone este repositório**
```bash
https://github.com/RamboFPS/Desafio-Criando-um-Sistema-Bancario-com-Python.git
