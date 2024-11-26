import tkinter as tk
from components.grid import Grid
from views.cadastro_produto import CadastroProduto

class GestaoProdutos(tk.Frame):
    def __init__(self, master, produto_controller):
        super().__init__(master)
        self.produto_controller = produto_controller
        self.pack(fill=tk.BOTH, expand=True)
        
        colunas = ["Nome", "Descrição", "Quantidade", "Valor"]
        self.dados = [(produto.nome, produto.descricao, produto.quantidade, produto.valor) for produto in produto_controller.listar_produtos()]
        
        self.lista_produtos = Grid(self, colunas, self.dados, self.editar_produto, self.excluir_produto)
        
        self.btn_cadastrar_produto = tk.Button(self, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.btn_cadastrar_produto.pack(pady=10)

    def cadastrar_produto(self):
        self.clear_frame()
        self.cadastro_produto_frame = CadastroProduto(self, self.produto_controller)
        self.cadastro_produto_frame.pack()

    def editar_produto(self, produto):
        self.clear_frame()
        self.cadastro_produto_frame = CadastroProduto(self, self.produto_controller, produto)
        self.cadastro_produto_frame.pack()

    def excluir_produto(self, produto):
        self.produto_controller.excluir_produto(produto[0])  # Supondo que o nome é o identificador único
        self.atualizar_lista()

    def atualizar_lista(self):
        self.dados = [(produto.nome, produto.descricao, produto.quantidade, produto.valor) for produto in self.produto_controller.listar_produtos()]
        self.lista_produtos.atualizar_lista(self.dados)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()