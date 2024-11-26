import tkinter as tk
from tkinter import messagebox

class RealizacaoVendas(tk.Frame):
    def __init__(self, master, venda_controller, produto_controller, usuario_controller):
        super().__init__(master)
        self.venda_controller = venda_controller
        self.produto_controller = produto_controller
        self.usuario_controller = usuario_controller
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_cliente = tk.Label(self, text="Cliente")
        self.label_cliente.pack()
        self.entry_cliente = tk.Entry(self)
        self.entry_cliente.pack()

        self.label_produto = tk.Label(self, text="Produto")
        self.label_produto.pack()
        self.entry_produto = tk.Entry(self)
        self.entry_produto.pack()

        self.label_quantidade = tk.Label(self, text="Quantidade")
        self.label_quantidade.pack()
        self.entry_quantidade = tk.Entry(self)
        self.entry_quantidade.pack()

        self.label_vendedor = tk.Label(self, text="Vendedor")
        self.label_vendedor.pack()
        self.entry_vendedor = tk.Entry(self)
        self.entry_vendedor.pack()

        self.label_forma_pagamento = tk.Label(self, text="Forma de Pagamento")
        self.label_forma_pagamento.pack()
        self.entry_forma_pagamento = tk.Entry(self)
        self.entry_forma_pagamento.pack()

        self.button_salvar = tk.Button(self, text="Salvar", command=self.salvar_venda)
        self.button_salvar.pack()

    def salvar_venda(self):
        cliente = self.entry_cliente.get()
        produto = self.entry_produto.get()
        quantidade = int(self.entry_quantidade.get())
        vendedor = self.entry_vendedor.get()
        forma_pagamento = self.entry_forma_pagamento.get()
        venda = self.venda_controller.cadastrar_venda(cliente, produto, quantidade, vendedor, forma_pagamento)
        messagebox.showinfo("Informação", f"Venda realizada com sucesso!")