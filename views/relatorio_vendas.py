import tkinter as tk
from tkinter import ttk

class RelatorioVendas(tk.Frame):
    def __init__(self, master, venda_controller):
        super().__init__(master)
        self.venda_controller = venda_controller
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("Cliente", "Produto", "Quantidade", "Vendedor", "Forma de Pagamento", "Data"), show="headings")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Vendedor", text="Vendedor")
        self.tree.heading("Forma de Pagamento", text="Forma de Pagamento")
        self.tree.heading("Data", text="Data")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.button_atualizar = tk.Button(self, text="Atualizar", command=self.atualizar_lista)
        self.button_atualizar.pack()

    def atualizar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for venda in self.venda_controller.listar_vendas():
            self.tree.insert("", tk.END, values=(venda.cliente, venda.produto, venda.quantidade, venda.vendedor, venda.forma_pagamento, venda.data_venda))