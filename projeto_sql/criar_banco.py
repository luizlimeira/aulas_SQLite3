import sqlite3
conn = sqlite3.connect('databaseloja.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS fornecedores(
            Id_Fornecedor INTEGER PRIMARY KEY,
            Nome TEXT,
            CNPJ TEXT,
            Email TEXT
        )   
''')

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS estoque_fornecedor(
                Id_Produto INTEGER PRIMARY KEY,
                Produto TEXT,
                Id_Fornecedor INT,
                Quantidade INT,
                FOREIGN KEY (Id_Fornecedor) REFERENCES fornecedores(Id_Fornecedor)
                
        )
''')


cursor.execute('''
        CREATE TABLE IF NOT EXISTS proprietarios(
                Id_Proprietario INTEGER PRIMARY KEY,
                Nome TEXT,
                CNPJ TEXT,
                Email TEXT
        )
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque_loja(
                ID INTEGER PRIMARY KEY,
                Id_Produto INT,
                Id_Proprietario INT,
                Quantidade INT,
                FOREIGN KEY (Id_Proprietario) REFERENCES proprietarios (Id_Proprietario),
                FOREIGN KEY (Id_Produto) REFERENCES estoque_fornecedor(Id_Produto)
        )
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas_fornecedor(
                Id_Venda_Fornecedor INTEGER PRIMARY KEY,
                Id_Produto INT,
                Quantidade INT,
                Preco_Unit REAL,
                Valor REAL,
                Data_venda DATE,
                FOREIGN KEY (Id_Produto) REFERENCES estoque_fornecedor (Id_Produto)
        )
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS id_vendas_fornecedor(
                ID INTEGER PRIMARY KEY,
                Id_venda INT,
                Id_fornecedor INT,
                Id_loja INT,
                FOREIGN KEY (Id_venda) REFERENCES vendas_fornecedor(Id_Venda_Fornecedor),
                FOREIGN KEY(Id_fornecedor) REFERENCES fornecedores(Id_Fornecedor),
                FOREIGN KEY(Id_loja) REFERENCES proprietarios(Id_Proprietario)
        )
''')


cursor.execute('''        
        CREATE TABLE IF NOT EXISTS clientes(
                Id_Cliente INTEGER PRIMARY KEY,
                Nome TEXT,
                Telefone TEXT,
                CPF TEXT,
                Email TEXT
        )
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas_cliente(
                Id_Venda INTEGER PRIMARY KEY,
                Id_Produto INT,
                Quantidade INT,
                Preco_Unit REAL,
                Valor REAL,
                Data_compra DATE,
                FOREIGN KEY (Id_Produto) REFERENCES estoque_fornecedor(Id_Produto)
        )
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS id_vendas_cliente(
               ID INTEGER PRIMARY KEY,
               Id_venda INT,
               Id_Loja INT,
               Id_Cliente INT,
               FOREIGN KEY (Id_venda) REFERENCES vendas_cliente(Id_Venda),
               FOREIGN KEY (Id_Loja) REFERENCES proprietarios(Id_Proprietario),
               FOREIGN KEY (Id_Cliente) REFERENCES clientes(Id_Cliente)
        )
''')

conn.commit()
conn.close()