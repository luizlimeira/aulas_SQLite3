import sqlite3

conn = sqlite3.connect('desafiobanco.db')

# criador de contas
def create_user():
    nome = input('Insira seu nome: ') # colocar o nome
    cpf = int(input('Insira CPF: ')) # colocar o cpf
    username = input('Crie um username: ') # colocar username
    senha = input('Crie uma senha: ') # colocar senha

    if verify_cpf(cpf) == True: # se o cpf não existir ele realiza a operação de verificar a senha

        if verify_password(senha) == True: # se a senha não existir ele realiza a operação de INSERT
            
            # INSERT de dados dos usuarios no banco
            conn.execute(f'''
                INSERT INTO usuarios (nome, cpf) VALUES ('{nome}', '{cpf}') 
            ''')

            # INSERT de dados das transações dos usuarios no banco
            conn.execute(f'''
                INSERT INTO transações (usuario_id, saldo,
                Depositos, Saques) VALUES(
                    (SELECT id FROM usuarios WHERE cpf = '{cpf}'),
                    0 , 0 , 0
                )
            ''')

            # INSERT das contas de login dos usuarios no banco
            conn.execute(f'''
            INSERT INTO senhas_usuarios (usuario_id, username, senhas) VALUES(
                (SELECT id FROM usuarios WHERE cpf = '{cpf}'), '{username}',
                '{senha}'
            )
        ''')

        else:
            create_user() # se a senha existir ele cancela a operação e repete 
    else:
        create_user() # se o cpf existir ele cancela a opreação e repete
    
    conn.commit()

# verificador de senha
def verify_password(senha): 
    query = conn.execute("SELECT * from senhas_usuarios")
    for i in query:
        query = i[3] # puxa a senha da lista de usuarios

    if senha in query: # verifica se a senha existe no banco de dados
        print("Senha muito comum, por favor, tente outra senha")
        print()
        return False # retorna False caso a senha exista no banco
    
    else:
        return True # retorna True caso a senha não exista no banco

#verificador de cpf
def verify_cpf(cpf):
    lista_querys = []
    query = conn.execute('SELECT * FROM usuarios')
    for i in query:
        query = i[2] # puxa o cpf da lista de usuarios
        lista_querys.append(query)
        
    if cpf in lista_querys: # verifica se o cpf existe no banco de dados
        print('CPF já cadastrado')
        print()
        return False # retorna False caso o cpf exista no banco

    else:
        return True # retorna True caso o cpf não existe no banco

# verificar saldo
def balance():
    login = input("Digite o login da sua conta: ") # insere username

    query = conn.execute(f"SELECT * FROM senhas_usuarios WHERE username = '{login}'") # puxa a senha atraves do username inserido pelo usuario
    result = query.fetchone() # puxa dados espeficios do banco de senhas_usuarios

    if result: # se o username existir no banco ele continua a operação
        senha = input("Digite sua senha: ") # insere senha

        if senha == result[3]: # verifica se a senha existe no banco e se está igual a senha inserida
            query1 = conn.execute(f"SELECT * FROM transações WHERE usuario_id = '{(result[1])}'\
            ORDER BY created_at DESC LIMIT 1")
            last_transaction = query1.fetchone() # puxa dados especificos da table de transações

            if last_transaction: # verifica se o id de usuario se encontra nas transações
                print('Seu Saldo é:', last_transaction[2])

        else: # se a senha não existir no banco printa e repete a operação
            print("Conta não encontrada, por favor, tente novamente")
            print()
        
    else: # se o login não existir no banco printa e repete e operação
        print("Conta não encontrada, por favor, tente novamente")
        print()
    
    conn.commit

# realizar a operação de depositar
def deposit():
    login = input("Digite o login da sua conta: ") # insere username

    query = conn.execute(f"SELECT * FROM senhas_usuarios WHERE username = '{login}'") # puxa a senha atraves do username inserido pelo usuario
    result = query.fetchone() # puxa dados especificos do banco de senhas_usuarios


    if result: # se o username existir no banco ele continua a operação
        senha = input("Digite sua senha: ") # insere senha

        if senha == result[3]: # verifica se a senha existe no banco e se está igual a senha inserida
            query1 = conn.execute(f"SELECT * FROM transações WHERE usuario_id = '{result[1]}'\
            ORDER BY created_at DESC LIMIT 1")
            transaction = query1.fetchone() # verifica se o id de usuario se encontra nas transações
            deposito = float(input('Quanto deseja depositar?: ')) # insere quanto deseja depositar
            
            if transaction: # verifica se o id de usuario se encontra nas transações
                conn.execute(f"INSERT INTO transações (usuario_id,\
                    saldo, Depositos, Saques) VALUES ('{result[1]}', '{transaction[2] + deposito}',\
                    '{deposito}' , '{transaction[4]}')") # insere os dados de acordo com o usuario_id na table de transações
           
        else: # se a senha não existir no banco printa e repete a operação
            print("Conta não encontrada, por favor, tente novamente")
            print()
    
    else: # se o login não existir no banco printa e repete e operação
        print("Conta não encontrada, por favor, tente novamente")
        print()

    conn.commit()

# realiza a operação de saque
def whithdraw():
    login = input("Digite o login da sua conta: ") # insere username

    query = conn.execute(f"SELECT * FROM senhas_usuarios WHERE username = '{login}'") # puxa a senha atraves do username inserido pelo usuario
    result = query.fetchone() # puxa dados especificos do banco de senhas_usuarios

    if result: # se o username existir no banco ele continua a operação
        senha = input("Digite sua senha: ") # insere senha

        if senha == result[3]: # verifica se a senha existe no banco e se está igual a senha inserida
            query1 = conn.execute(f"SELECT * FROM transações WHERE usuario_id = {result[1]}\
            ORDER BY created_at DESC LIMIT 1") # puxa dados especificos da table de transações verificando o saldo mais recente
            transaction = query1.fetchone() # verifica se o id de usuario se encontra nas transações
            saque = float(input('Quanto deseja sacar?: ')) # insere quanto deseja sacar
        
            if saque <= transaction[2]: # verifica se o saque é maior que o saldo na conta
                conn.execute(f"INSERT INTO transações (usuario_id,\
                    saldo, Depositos, Saques)\
                    VALUES ('{result[1]}', '{transaction[2] - saque}',\
                    '{transaction[3]}' , '{saque}')") # insere dados de acordo com o usuario_id na table de transações
            
            else: # printa caso o saldo seja insuficiente para o saque
                print("Saldo insuficiente")
        
        else: # se a senha não existir no banco printa e repete a operação
            print("Conta não encontrada, por favor, tente novamente")
            print()
    
    else: # se o login não existir no banco printa e repete e operação
        print("Conta não encontrada, por favor, tente novamente")
        print()

    conn.commit()

def break_program(): # encerra o programa e fecha a conexão com o banco
    print("Programa encerrado. Obrigado!")
    conn.close()
