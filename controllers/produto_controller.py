from db.models import Produto
#from db.crud import CRUD

class ProdutoController:
    def __init__(self):
        #self.crud = CRUD()
        self.tabela = "produtos"
        self.colunas = ["id", "nome", "descricao", "quantidade", "valor"]
        self.produtos = []
        self.next_id = 1  # Inicializa o próximo ID
        produtos_teste = [
            {"nome": "Produto A", "descricao": "Descrição do Produto A", "quantidade": 10, "valor": 100.0},
            {"nome": "Produto B", "descricao": "Descrição do Produto B", "quantidade": 20, "valor": 200.0},
            {"nome": "Produto C", "descricao": "Descrição do Produto C", "quantidade": 30, "valor": 300.0},
            {"nome": "Produto D", "descricao": "Descrição do Produto D", "quantidade": 40, "valor": 400.0},
            {"nome": "Produto E", "descricao": "Descrição do Produto E", "quantidade": 50, "valor": 500.0},
            {"nome": "Produto F", "descricao": "Descrição do Produto F", "quantidade": 60, "valor": 600.0},
            {"nome": "Produto G", "descricao": "Descrição do Produto G", "quantidade": 70, "valor": 700.0},
            {"nome": "Produto H", "descricao": "Descrição do Produto H", "quantidade": 80, "valor": 800.0},
            {"nome": "Produto I", "descricao": "Descrição do Produto I", "quantidade": 90, "valor": 900.0},
            {"nome": "Produto J", "descricao": "Descrição do Produto J", "quantidade": 100, "valor": 1000.0}
        ]
        for produto in produtos_teste:
            self.cadastrar_produto(produto["nome"], produto["descricao"], produto["quantidade"], produto["valor"])

    def cadastrar_produto(self, nome, descricao, quantidade, valor):
        produto = Produto(self.next_id, nome, descricao, quantidade, valor)
        self.produtos.append(produto)
        self.next_id += 1
        # Descomente as linhas abaixo para usar o banco de dados
        # valores = (nome, descricao, quantidade, valor)
        # self.crud.criar(self.tabela, self.colunas[1:], valores)  # Exclui o 'id'
        return produto

    def listar_produtos(self):
        # Descomente as linhas abaixo para usar o banco de dados
        # produtos = self.crud.listar(self.tabela, self.colunas)
        # return [Produto(*produto) for produto in produtos]
        return self.produtos

    def buscar_produto_por_id(self, id):
        # Descomente as linhas abaixo para usar o banco de dados
        # produto = self.crud.buscar_por_id(self.tabela, self.colunas, "id", id)
        # if produto:
        #     return Produto(*produto)
        return next((produto for produto in self.produtos if produto.id == id), None)

    def buscar_produto_por_nome(self, nome):
        # Descomente as linhas abaixo para usar o banco de dados
        # condicao = "nome LIKE %s"
        # valores = (f"%{nome}%",)
        # produtos = self.crud.buscar_por_condicao(self.tabela, self.colunas, condicao, valores)
        # return [Produto(*produto) for produto in produtos]
        return [produto for produto in self.produtos if nome.lower() in produto.nome.lower()]

    def atualizar_produto(self, id, nome, descricao, quantidade, valor):
        # Descomente as linhas abaixo para usar o banco de dados
        # valores = (nome, descricao, quantidade, valor)
        # self.crud.atualizar(self.tabela, self.colunas[1:], valores, "id", id)  # Exclui o 'id'
        produto = self.buscar_produto_por_id(id)
        if produto:
            produto.nome = nome
            produto.descricao = descricao
            produto.quantidade = quantidade
            produto.valor = valor

    def excluir_produto(self, id):
        # Descomente as linhas abaixo para usar o banco de dados
        # self.crud.excluir(self.tabela, "id", id)
        self.produtos = [produto for produto in self.produtos if produto.id != id]