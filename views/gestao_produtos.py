import tkinter as tk
from components.grid import Grid
from views.cadastro_produto import CadastroProduto

class GestaoProdutos(tk.Frame):
    def __init__(self, master, produto_controller):
        super().__init__(master)
        self.produto_controller = produto_controller
        self.showGrid(produto_controller)
        
    def showGrid(self, produto_controller):
        self.pack(fill=tk.BOTH, expand=True)
        colunas = ["ID", "Nome", "Descrição", "Quantidade", "Valor"]
        self.dados = [(produto.id, produto.nome, produto.descricao, produto.quantidade, produto.valor) for produto in produto_controller.listar_produtos()]

        self.mensagem_titulo = tk.Label(self, text="Gerenciamento de Produtos", fg="blue", font=("Arial", 16))
        self.mensagem_titulo.pack(pady=10)

        self.mensagem_label = tk.Label(self, text="", fg="red")
        self.mensagem_label.pack(pady=5)

        # Criar frame para os botões
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X)

        self.btn_cadastrar_produto = tk.Button(button_frame, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.btn_cadastrar_produto.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_editar_produto = tk.Button(button_frame, text="Editar Produto", state=tk.DISABLED, command=self.editar_produto_selecionado)
        self.btn_editar_produto.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_excluir_produto = tk.Button(button_frame, text="Excluir Produto", state=tk.DISABLED, command=self.excluir_produto_selecionado)
        self.btn_excluir_produto.pack(side=tk.LEFT, padx=5, pady=5)

        # Criar a grid
        self.lista_produtos = Grid(self, colunas, self.dados)

        # Vincular evento de seleção na grid para ativar/desativar botões
        self.lista_produtos.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def cadastrar_produto(self):
        self.clear_frame()
        self.cadastro_produto_frame = CadastroProduto(self, self.produto_controller)
        self.cadastro_produto_frame.pack()

    def editar_produto(self, produto):
        self.clear_frame()
        produto_obj = self.produto_controller.buscar_produto_por_id(produto[0])
        self.cadastro_produto_frame = CadastroProduto(self, self.produto_controller, produto_obj)
        self.cadastro_produto_frame.pack()

    def excluir_produto(self, produto):
        self.produto_controller.excluir_produto(produto[0])  # Usando o ID para exclusão
        self.atualizar_lista()

    def editar_produto_selecionado(self):
        selected_item = self.lista_produtos.tree.selection()[0]
        produto_id = self.lista_produtos.tree.item(selected_item)['values'][0]
        produto_obj = self.produto_controller.buscar_produto_por_id(produto_id)
        self.editar_produto((produto_obj.id, produto_obj.nome, produto_obj.descricao, produto_obj.quantidade, produto_obj.valor))

    def excluir_produto_selecionado(self):
        selected_item = self.lista_produtos.tree.selection()[0]
        produto_id = self.lista_produtos.tree.item(selected_item)['values'][0]
        self.excluir_produto((produto_id,))

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def atualizar_lista(self):
        print("Atualizando lista...")
        self.clear_frame()
        self.showGrid(self.produto_controller)

    def mostrar_mensagem(self, mensagem, tipo):
        print(mensagem)
        if tipo == "sucesso":
            self.mensagem_label.config(text=mensagem, fg="green")
        else:
            self.mensagem_label.config(text=mensagem, fg="red")

    def on_tree_select(self, event):
        if self.lista_produtos.tree.selection():
            self.btn_editar_produto.config(state=tk.NORMAL)
            self.btn_excluir_produto.config(state=tk.NORMAL)
        else:
            self.btn_editar_produto.config(state=tk.DISABLED)
            self.btn_excluir_produto.config(state=tk.DISABLED)