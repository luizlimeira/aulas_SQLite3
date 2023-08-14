import sqlite3

conn = sqlite3.connect('desafiobanco.db')
cursor = conn.cursor()

#Criando a tabela "usuarios" com chave primaria "id"
cursor.execute('''
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        cpf INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE transações(
        id INTEGER PRIMARY KEY,
        usuario_id INTEGER,
        saldo REAL,
        Depositos REAL,
        Saques REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) 
    )    
''')

cursor.execute('''
    CREATE TABLE senhas_usuarios(
        id INTEGER PRIMARY KEY,
        usuario_id INTEGER,
        username TEXT,
        senhas TEXT,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)     
    )    
''')

conn.close