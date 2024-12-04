import requests
from controllers.models import Produto

class ProdutoController:
    def __init__(self):
        self.api_url = "http://localhost:5000/produtos"
        self.produtos = []
        self.next_id = 1  # Inicializa o próximo ID

    def cadastrar_produto(self, nome, descricao, quantidade, valor):
        data = {"nome": nome, "descricao": descricao, "quantidade": quantidade, "valor": valor}
        response = requests.post(self.api_url, json=data)
        if response.status_code == 201:
            produto_data = response.json()
            produto = Produto(produto_data['id'], nome, descricao, quantidade, valor)
            self.produtos.append(produto)
            return produto
        else:
            print(f"Erro ao cadastrar produto: {response.json()}")
            return None

    def listar_produtos(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            produtos_data = response.json()
            self.produtos = [Produto(produto['id'], produto['nome'], produto['descricao'], produto['quantidade'], produto['valor']) for produto in produtos_data]
            return self.produtos
        else:
            print(f"Erro ao listar produtos: {response.json()}")
            return []

    def buscar_produto_por_id(self, id):
        response = requests.get(f"{self.api_url}/{id}")
        if response.status_code == 200:
            produto_data = response.json()
            return Produto(produto_data['id'], produto_data['nome'], produto_data['descricao'], produto_data['quantidade'], produto_data['valor'])
        else:
            print(f"Erro ao buscar produto por ID: {response.json()}")
            return None

    def buscar_produto_por_nome(self, nome):
        response = requests.get(self.api_url, params={"nome": nome})
        if response.status_code == 200:
            produtos_data = response.json()
            return [Produto(produto['id'], produto['nome'], produto['descricao'], produto['quantidade'], produto['valor']) for produto in produtos_data]
        else:
            print(f"Erro ao buscar produto por nome: {response.json()}")
            return []

    def atualizar_produto(self, id, nome, descricao, quantidade, valor):
        data = {"nome": nome, "descricao": descricao, "quantidade": quantidade, "valor": valor}
        response = requests.put(f"{self.api_url}/{id}", json=data)
        if response.status_code == 200:
            produto = self.buscar_produto_por_id(id)
            if produto:
                produto.nome = nome
                produto.descricao = descricao
                produto.quantidade = quantidade
                produto.valor = valor
        else:
            print(f"Erro ao atualizar produto: {response.json()}")

    def excluir_produto(self, id):
        response = requests.delete(f"{self.api_url}/{id}")
        if response.status_code == 200:
            self.produtos = [produto for produto in self.produtos if produto.id != id]
        else:
            print(f"Erro ao excluir produto: {response.json()}")