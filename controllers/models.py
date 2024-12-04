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

    def to_dict(self):
        return {
            'id': self.get_id(),
            'nome': self.get_nome(),
            'cpf': self.get_cpf(),
            'endereco': self.get_endereco()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['nome'], data['cpf'], data['endereco'])


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

    def to_dict(self):
        return {
            'id': self.get_id(),
            'nome': self.get_nome(),
            'login': self.get_login(),
            'senha': self.get_senha(),
            'tipo': self.get_tipo()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['nome'], data['login'], data['senha'], data['tipo'])


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

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'quantidade': self.quantidade,
            'valor': self.valor
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['nome'], data['descricao'], data['quantidade'], data['valor'])


class ItemVenda:
    def __init__(self, venda_id, produto_id, quantidade, valor_unitario):
        self.venda_id = venda_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario

    def to_dict(self):
        return {
            'venda_id': self.venda_id,
            'produto_id': self.produto_id,
            'quantidade': self.quantidade,
            'valor_unitario': self.valor_unitario
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['venda_id'], data['produto_id'], data['quantidade'], data['valor_unitario'])

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
        quantidade = int(quantidade)
        valor_unitario = float(valor_unitario)
        if quantidade > 0:
            item_venda = ItemVenda(self.id, produto_id, quantidade, valor_unitario)
            self.itens.append(item_venda)

    def gerar_relatorio(self, cliente_controller, usuario_controller):
        cliente = cliente_controller.buscar_cliente_por_id(self.cliente_id)
        vendedor = usuario_controller.buscar_usuario_por_id(self.vendedor_id)
        return {
            'id': self.id,
            'cliente': cliente.get_nome() if cliente else 'Desconhecido',
            'vendedor': vendedor.get_nome() if vendedor else 'Desconhecido',
            'produtos': [item.produto_id for item in self.itens],
            'valor_total': sum(item.quantidade * item.valor_unitario for item in self.itens),
            'data_venda': self.data_venda
        }

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'vendedor_id': self.vendedor_id,
            'data_venda': self.data_venda,
            'forma_pagamento': self.forma_pagamento,
            'quantidade_parcelas': self.quantidade_parcelas,
            'itens': [item.to_dict() for item in self.itens]
        }

    @classmethod
    def from_dict(cls, data):
        venda = cls(data['id'], data['cliente_id'], data['vendedor_id'], data['data_venda'], data['forma_pagamento'], data.get('quantidade_parcelas'))
        venda.itens = [ItemVenda.from_dict(item) for item in data.get('itens', [])]
        return venda