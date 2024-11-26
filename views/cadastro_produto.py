import tkinter as tk
from components.formulario_cadastro import FormularioCadastro

class CadastroProduto(tk.Frame):
    def __init__(self, master, produto_controller, produto=None):
        super().__init__(master)
        self.produto_controller = produto_controller
        self.produto = produto
        campos = ["Nome", "Descrição", "Quantidade", "Valor"]
        
        self.formulario = FormularioCadastro(self, campos, self.salvar_produto)
        
        if produto:
            self.preencher_dados(produto)

    def preencher_dados(self, produto):
        self.formulario.set_dados({
            "Nome": produto.nome,
            "Descrição": produto.descricao,
            "Quantidade": produto.quantidade,
            "Valor": produto.valor
        })

    def salvar_produto(self, dados):
        nome = dados["Nome"]
        descricao = dados["Descrição"]
        quantidade = int(dados["Quantidade"])
        valor = float(dados["Valor"])
        
        if self.produto:
            # Atualizar o produto existente
            self.produto_controller.atualizar_produto(self.produto.id, nome, descricao, quantidade, valor)
        else:
            # Cadastrar um novo produto
            self.produto_controller.cadastrar_produto(nome, descricao, quantidade, valor)