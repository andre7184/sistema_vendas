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

        self.container = tk.Frame(self, bg="#D3D3D3")  # Adiciona uma borda cinza e padding interno
        self.container.pack(fill=tk.BOTH, expand=True)

        self.lista_produtos = Grid(self.container, colunas, self.dados, self.editar_produto, self.excluir_produto)
        
        self.btn_cadastrar_produto = tk.Button(self, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.btn_cadastrar_produto.pack(pady=10)

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