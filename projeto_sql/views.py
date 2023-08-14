from funcoesloja import *

def criar_cliente(request):
    nome_cliente = request.POST.get('nome_cliente')
    tel_cliente = request.POST.get('tel_cliente')
    email_cliente = request.POST.get('email_cliente')
    cpf_cliente = request.POST.get('cpf_cliente')

    inserir_cliente(nome_cliente, tel_cliente, email_cliente, cpf_cliente)

def criar_proprietario(request):
    nome_proprietario = request.POST.get('nome_proprietario')
    cnpj_proprietario = request.POST.get('cnpj_proprietario')
    email_proprietario = request.POST.get('email_proprietario')

    inserir_proprietario(nome_proprietario, cnpj_proprietario, email_proprietario)

def criar_fornecedor(request):
    nome_fornecedor = request.POST.get('nome_fornecedor')
    cnpj_fornecedor = request.POST.get('cnpj_fornecedor')
    email_fornecedor = request.POST.get('email_fornecedor')

    inserir_fornecedor(nome_fornecedor, cnpj_fornecedor, email_fornecedor)

def fornecedor_estoque(request):
    produto = request.POST.get('produto_fornecedor')
    quantidade = request.POST.get('qtd_produto')
    cnpj = request.POST.get('cnpj_fornecedor_estoque')

    estoque_fornecedor(produto, quantidade, cnpj)

def fornecedor_venda(request):
    nome_produto = request.POST.get('nome_produto_fornecedor')
    cnpj_fornecedor = request.POST.get('cnpj_fornecedor_venda')
    cnpj_proprietario = request.POST.get('cnpj_proprietario')
    quantidade = request.POST.get('qtd_venda_fornecedor')
    preco = request.POST.get('preco_venda_fornecedor')
    data = request.POST.get('data_venda_fornecedor')

    vendas_fornecedor(nome_produto, cnpj_fornecedor, cnpj_proprietario, quantidade, preco, data)

def cliente_venda(request):
    nome_produto = request.POST.get('nome_produto_cliente')
    cpf_cliente = request.POST.get('cpf_cliente_venda')
    cnpj_fornecedor = request.POST.get('cnpj_fornecedor_cliente')
    quantidade = request.POST.get('qtd_venda_cliente')
    preco = request.POST.get('preco_venda_cliente')
    data = request.POST.get('data_venda_cliente')

    vendas_cliente(nome_produto, cpf_cliente, cnpj_fornecedor, quantidade, preco, data)