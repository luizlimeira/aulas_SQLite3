import sqlite3
conn = sqlite3.connect('databaseloja.db', check_same_thread= False)
cursor = conn.cursor()


def inserir_fornecedor(nome_fornecedor, cnpj_fornecedor, email_fornecedor):
    query = cursor.execute('''SELECT CNPJ FROM main_fornecedores''')
    lista_query = []
    for i in query:
        lista_query.append(i[0])
        
    nome = nome_fornecedor
    cnpj = cnpj_fornecedor

    if cnpj in lista_query:
        print("CNPJ já cadastrado.")

    else:
        email = email_fornecedor
        cursor.execute(f"INSERT INTO main_fornecedores (nome, cnpj, email) VALUES ('{nome}','{cnpj}', '{email}')")

    conn.commit()


def inserir_proprietario(nome_proprietario, cnpj_proprietario, email_proprietario):
    query = cursor.execute('''SELECT CNPJ FROM main_proprietarios''')
    lista_query = []
    for i in query:
        lista_query.append(i[0])
        
    nome = nome_proprietario
    cnpj = cnpj_proprietario

    if cnpj in lista_query:
        print('CNPJ já cadastrado.')

    else:
        email = email_proprietario
        cursor.execute(f"INSERT INTO main_proprietarios (nome, cnpj, email) VALUES ('{nome}', '{cnpj}', '{email}') ")

    conn.commit()


def inserir_cliente(nome_cliente, tel_cliente, email_cliente, cpf_cliente):
    query = cursor.execute('''
            SELECT CPF from main_clientes
    ''')
    lista_query = []
    for i in query:
        lista_query.append(i[0])

    nome = nome_cliente
    telefone = tel_cliente
    email = email_cliente
    cpf = cpf_cliente
    print('cheguei aqui:', nome, telefone)
    if cpf in lista_query:
        print("CPF já cadastrado.")

    else:
        cursor.execute(f"INSERT INTO main_clientes (nome, telefone, cpf, email) VALUES ('{nome}', '{telefone}', '{cpf}', '{email}')")

    conn.commit()


def estoque_fornecedor(produto_fornecedor, quantidade_produto, cnpj):
    produto = produto_fornecedor
    quantidade = quantidade_produto
    cnpj_fornecedor = cnpj
    
    fornecedor = cursor.execute(f"SELECT Id_fornecedor FROM main_fornecedores WHERE cnpj = '{cnpj_fornecedor}'")
    fornecedor = fornecedor.fetchone()

    if produto == produto:
        quantidade_estoque = cursor.execute(f"SELECT quantidade FROM main_estoquefornecedor WHERE produto = '{produto}'")
        quantidade_estoque = quantidade_estoque.fetchone()

        if quantidade_estoque is not None:
            if fornecedor is not None:
                nova_quantidade = quantidade + quantidade_estoque[0]
                cursor.execute(f"UPDATE main_estoquefornecedor SET quantidade = {nova_quantidade} WHERE produto = '{produto}' ")
            else: 
                print('CNPJ não encontrado. Digite novamente')
                print()
                       
        else:      
            if fornecedor is not None:                     
                cursor.execute(f"INSERT INTO main_estoquefornecedor (produto, Id_fornecedor, quantidade) VALUES ('{produto}','{fornecedor[0]}',{quantidade})")                
            else:
                print('CNPJ não encontrado. Digite novamente')
                print()
                
        

    conn.commit()


def vendas_fornecedor(produto_nome, fornecedor_cnpj, proprietario_cnpj, quantidade_produto, preco_produto, data):
    nome_produto = produto_nome
    produto = cursor.execute(f"SELECT Id_Produto FROM estoque_fornecedor WHERE Produto = '{nome_produto}' ")
    produto = produto.fetchone()

    cnpj_fornecedor = fornecedor_cnpj
    query5 = cursor.execute(f"SELECT Id_Fornecedor FROM fornecedores WHERE CNPJ = '{cnpj_fornecedor}'")
    query5 = query5.fetchone()
    cnpj_proprietario = proprietario_cnpj
    proprietario = cursor.execute(f"SELECT Id_proprietario FROM proprietarios WHERE cnpj = '{cnpj_proprietario}'")
    proprietario = proprietario.fetchone()

    quantidade = quantidade_produto
    preco_unit = preco_produto
    valor = quantidade * preco_unit
    data_venda = data

    query = cursor.execute(f'''SELECT Quantidade FROM estoque_fornecedor WHERE Produto = '{nome_produto}' ''')
    quantidade_fornecedor = query.fetchone()

    query2 = cursor.execute(f"SELECT Id_Produto FROM estoque_loja")
    lista_query = []
    for i in query2:
        lista_query.append(i[0])

    query3 = cursor.execute(f"SELECT Quantidade FROM estoque_loja WHERE Id_produto = '{produto[0]}'")
    query3 = query3.fetchone()

    if produto is not None:
        if proprietario is not None:
            if query5 is not None:
                if quantidade_fornecedor[0] > quantidade:
                    if produto[0] in lista_query:
                        nova_quatidade = query3[0] + quantidade
                        cursor.execute(f"UPDATE estoque_loja SET Quantidade = ({nova_quatidade}) WHERE Id_Produto = '{produto[0]}'")

                        cursor.execute(f"INSERT INTO vendas_fornecedor (Id_produto,\
                        quantidade, preco_unit, valor, data_venda)\
                        VALUES ('{produto[0]}','{quantidade}',\
                        '{preco_unit}', '{valor}', '{data_venda}')")

                        cursor.execute(f"UPDATE estoque_fornecedor SET Quantidade = ({quantidade_fornecedor[0] - quantidade}) WHERE Id_Produto = '{produto[0]}' ")

                    else:
                        cursor.execute(f"INSERT INTO estoque_loja (Id_produto, Id_proprietario, quantidade) VALUES ('{produto[0]}','{proprietario[0]}','{quantidade}')")

                        cursor.execute(f"INSERT INTO vendas_fornecedor (Id_produto,\
                        quantidade, preco_unit, valor, data_venda)\
                        VALUES ('{produto[0]}','{quantidade}',\
                        '{preco_unit}', '{valor}', '{data_venda}')")

                        conn.commit()

                        query4 = cursor.execute(f"SELECT Id_Venda_Fornecedor FROM vendas_fornecedor WHERE Id_Produto = '{produto[0]}'")
                        query4 = query4.fetchone()

                        cursor.execute(f"UPDATE estoque_fornecedor SET Quantidade = ({quantidade_fornecedor[0] - quantidade}) WHERE Id_Produto = '{produto[0]}' ")

                        cursor.execute(f"INSERT INTO id_vendas_fornecedor (Id_venda,\
                        Id_fornecedor, Id_loja) VALUES ('{query4[0]}', '{query5[0]}', '{proprietario[0]}')\
                        ")

                else:
                    return False

            else:
                return False

        else:
            return False
            
    else:
        return False
        
    conn.commit()


def vendas_cliente(produto_nome, cpf_cliente, proprietario_cnpj, quantidade_produto, preco_produto, data):
    nome_produto = produto_nome
    produto = cursor.execute(f"SELECT Id_Produto FROM estoque_fornecedor WHERE produto = '{nome_produto}'")
    produto = produto.fetchone()

    cpf = cpf_cliente
    query1 = cursor.execute(f'SELECT Id_Cliente FROM clientes WHERE cpf = "{cpf}"')
    query1 = query1.fetchone()

    cnpj_proprietario = proprietario_cnpj

    quantidade = quantidade_produto
    preco_unit = preco_produto
    valor = quantidade * preco_unit
    data_compra = data

    query2 = cursor.execute('SELECT * FROM vendas_cliente')
    query2 = query2.fetchone()

    query3 = cursor.execute(f'SELECT * FROM proprietarios WHERE CNPJ = "{cnpj_proprietario}"')
    query3 = query3.fetchone()

    query4 = cursor.execute('SELECT * FROM clientes')
    query4 = query4.fetchone()

    query = cursor.execute(f"Select Quantidade FROM estoque_loja WHERE Id_Produto = '{produto[0]}' ")
    quantidade_proprietario = query.fetchone()

    if produto is not None:
        if query1 is not None:
            if query3 is not None:

                if quantidade_proprietario[0] < quantidade:
                    print('Quantidade insuficiente. Tente Novamente')

                else:    
                    cursor.execute(f"INSERT INTO vendas_cliente (Id_produto, quantidade,\
                    preco_unit, valor, data_compra) VALUES\
                    ('{produto[0]}','{quantidade}', '{preco_unit}', '{valor}',\
                    '{data_compra}')")

                    conn.commit()

                    query2 = cursor.execute('SELECT * FROM vendas_cliente')
                    query2 = query2.fetchone()

                    cursor.execute(f"INSERT INTO id_vendas_cliente (Id_venda, Id_loja, Id_cliente)\
                        VALUES ('{query2[0]}', '{query3[0]}', '{query4[0]}')")

                    cursor.execute(f'''UPDATE estoque_loja SET Quantidade = ({quantidade_proprietario[0] - quantidade}) WHERE Id_Produto = "{produto[0]}" ''')
            
            else:
                return False

        else:
            return False

    else:
        return False

    conn.commit()