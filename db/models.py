class Pessoa:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco

class Usuario(Pessoa):
    def __init__(self, nome, cpf, endereco, login, senha, tipo):
        super().__init__(nome, cpf, endereco)
        self.login = login
        self.senha = senha
        self.tipo = tipo

class Cliente(Pessoa):
    def __init__(self, nome, cpf, endereco):
        super().__init__(nome, cpf, endereco)

class Produto:
    def __init__(self, nome, descricao, quantidade, valor):
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor

class Venda:
    def __init__(self, cliente, vendedor, data_venda, forma_pagamento, quantidade_parcelas=None):
        self.cliente = cliente
        self.vendedor = vendedor
        self.data_venda = data_venda
        self.forma_pagamento = forma_pagamento
        self.quantidade_parcelas = quantidade_parcelas
        self.itens = []

    def adicionar_item(self, produto, quantidade, valor_unitario):
        self.itens.append({
            'produto': produto,
            'quantidade': quantidade,
            'valor_unitario': valor_unitario
        })