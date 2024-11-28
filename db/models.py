class Pessoa:
    def __init__(self, id, nome, cpf, endereco):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco

class Usuario(Pessoa):
    def __init__(self, id, nome, login, senha, tipo):
        super().__init__(id, nome, None, None)
        self.login = login
        self.senha = senha
        self.tipo = tipo

class Cliente(Pessoa):
    def __init__(self, id, nome, cpf, endereco):
        super().__init__(id, nome, cpf, endereco)

class Produto:
    def __init__(self, id, nome, descricao, quantidade, valor):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor = valor

class Venda:
    def __init__(self, id, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas=None):
        self.id = id
        self.cliente_id = cliente_id
        self.vendedor_id = vendedor_id
        self.data_venda = data_venda
        self.forma_pagamento = forma_pagamento
        self.quantidade_parcelas = quantidade_parcelas
        self.itens = []

    def adicionar_item(self, produto_id, quantidade, valor_unitario):
        self.itens.append({
            'produto_id': produto_id,
            'quantidade': quantidade,
            'valor_unitario': valor_unitario
        })

    def gerar_relatorio(self):
        return Relatorio(
            id=self.id,
            cliente=self.cliente_id,
            vendedor=self.vendedor_id,
            produto=[item['produto_id'] for item in self.itens],
            valor=sum(item['quantidade'] * item['valor_unitario'] for item in self.itens),
            data_venda=self.data_venda
        )

class Relatorio:
    def __init__(self, id, cliente, vendedor, produto, valor, data_venda):
        self.id = id
        self.cliente = cliente
        self.vendedor = vendedor
        self.produto = produto
        self.valor = valor
        self.data_venda = data_venda

class SistemaVendas:
    def __init__(self):
        self.usuarios = []
        self.clientes = []
        self.produtos = []
        self.vendas = []
        self.relatorios = []

    def adicionar_usuario(self, id, nome, login, senha, tipo):
        usuario = Usuario(id, nome, login, senha, tipo)
        self.usuarios.append(usuario)

    def adicionar_cliente(self, id, nome, cpf, endereco):
        cliente = Cliente(id, nome, cpf, endereco)
        self.clientes.append(cliente)

    def adicionar_produto(self, id, nome, descricao, quantidade, valor):
        produto = Produto(id, nome, descricao, quantidade, valor)
        self.produtos.append(produto)

    def adicionar_venda(self, id, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas=None):
        venda = Venda(id, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas)
        self.vendas.append(venda)
        relatorio = venda.gerar_relatorio()
        self.relatorios.append(relatorio)

    def adicionar_item_venda(self, venda_id, produto_id, quantidade, valor_unitario):
        venda = next((v for v in self.vendas if v.id == venda_id), None)
        if venda:
            venda.adicionar_item(produto_id, quantidade, valor_unitario)