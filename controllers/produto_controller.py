from db.models import Produto
# from db.connection import get_connection

class ProdutoController:
    def __init__(self):
        self.produtos = []

    def cadastrar_produto(self, nome, descricao, quantidade, valor):
        produto = Produto(nome, descricao, quantidade, valor)
        self.produtos.append(produto)
        # Descomente as linhas abaixo para usar o banco de dados
        # conn = get_connection()
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO produtos (nome, descricao, quantidade, valor) VALUES (%s, %s, %s, %s)",
        #                (produto.nome, produto.descricao, produto.quantidade, produto.valor))
        # conn.commit()
        # cursor.close()
        # conn.close()
        return produto

    def listar_produtos(self):
        # Descomente as linhas abaixo para usar o banco de dados
        # conn = get_connection()
        # cursor = conn.cursor()
        # cursor.execute("SELECT nome, descricao, quantidade, valor FROM produtos")
        # produtos = cursor.fetchall()
        # cursor.close()
        # conn.close()
        # return [Produto(nome, descricao, quantidade, valor) for nome, descricao, quantidade, valor in produtos]
        return self.produtos