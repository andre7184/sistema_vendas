import tkinter as tk
from tkinter import ttk

from components.itens import adjust_column_width, criar_frame

class Grid(tk.Frame):
    def __init__(self, master, colunas, dados, height=None):
        super().__init__(master)
        self.height = height
        self.colunas = colunas
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets(colunas, dados)

    def create_widgets(self, colunas, dados):
        frame = criar_frame(self, Grid, padding=5, preencher=tk.BOTH, expandir=True)#ttk.Frame(self)
        #frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(frame, columns=colunas, show='headings', height=self.height)
        for col in colunas:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, anchor=tk.CENTER, width=50)
            else:
                self.tree.column(col, anchor=tk.CENTER)

        for row in dados:
            self.tree.insert('', tk.END, values=row)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        adjust_column_width(self.tree)

    def add_row(self, dados):
        self.tree.insert('', tk.END, values=dados)

    def remove_row(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item[0])

    def update_row(self, item, dados):
        self.tree.item(item, values=dados)

    def update_data(self, dados):
        # Limpar todos os dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Inserir novos dados
        for row in dados:
            self.tree.insert('', tk.END, values=row)

    def atualizar_dados(self, dados):
        # Limpar os dados existentes na Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Inserir os novos dados
        for item in dados:
            self.tree.insert('', tk.END, values=item)

    def obter_dados(self):
        dados = []
        for row_id in self.tree.get_children():
            row = self.tree.item(row_id)['values']
            dados.append(row)
        return dados
