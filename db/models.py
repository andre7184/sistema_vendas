class Pessoa:
    def __init__(self, id, nome, cpf, endereco):
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._endereco = endereco

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_cpf(self):
        return self._cpf

    def get_endereco(self):
        return self._endereco

    def set_nome(self, nome):
        self._nome = nome

    def set_cpf(self, cpf):
        self._cpf = cpf

    def set_endereco(self, endereco):
        self._endereco = endereco


class Usuario(Pessoa):
    def __init__(self, id, nome, login, senha, tipo):
        super().__init__(id, nome, None, None)
        self.__login = login
        self.__senha = senha
        self.__tipo = tipo

    def get_login(self):
        return self.__login

    def get_senha(self):
        return self.__senha

    def get_tipo(self):
        return self.__tipo

    def set_login(self, login):
        self.__login = login

    def set_senha(self, senha):
        self.__senha = senha

    def set_tipo(self, tipo):
        self.__tipo = tipo


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
        quantidade = int(quantidade)  # Certifique-se de que a quantidade seja um inteiro
        valor_unitario = float(valor_unitario)  # Certifique-se de que o valor unitário seja um float
        if quantidade > 0:
            self.itens.append({
                'produto_id': produto_id,
                'quantidade': quantidade,
                'valor_unitario': valor_unitario
            })

    def gerar_relatorio(self, cliente_controller, usuario_controller):
        cliente = cliente_controller.buscar_cliente_por_id(self.cliente_id)
        vendedor = usuario_controller.buscar_usuario_por_id(self.vendedor_id)
        return {
            'id': self.id,
            'cliente': cliente.get_nome() if cliente else 'Desconhecido',
            'vendedor': vendedor.get_nome() if vendedor else 'Desconhecido',
            'produtos': [item['produto_id'] for item in self.itens],
            'valor_total': sum(item['quantidade'] * item['valor_unitario'] for item in self.itens),
            'data_venda': self.data_venda
        }

class SistemaVendas:
    def __init__(self):
        self.usuarios = []
        self.clientes = []
        self.produtos = []
        self.vendas = []

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

    def adicionar_item_venda(self, venda_id, produto_id, quantidade, valor_unitario):
        venda = next((v for v in self.vendas if v.id == venda_id), None)
        if venda:
            venda.adicionar_item(produto_id, quantidade, valor_unitario)

    def gerar_relatorio_venda(self, venda_id):
        venda = next((v for v in self.vendas if v.id == venda_id), None)
        if venda:
            return venda.gerar_relatorio(self)
        return None