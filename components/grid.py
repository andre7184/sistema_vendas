import tkinter as tk
from tkinter import ttk

class Grid(tk.Frame):
    def __init__(self, master, colunas, dados, editar_callback, excluir_callback):
        super().__init__(master)
        self.editar_callback = editar_callback
        self.excluir_callback = excluir_callback
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets(colunas, dados)

    def create_widgets(self, colunas, dados):
        # Adiciona a coluna 'Ações' às colunas
        colunas.append('Ações')

        # Cria um frame para a tabela
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, expand=True, padx=10, pady=10, anchor='n')

        # Cria os cabeçalhos da tabela
        for col in range(len(colunas)):
            header = ttk.Label(frame, text=colunas[col], borderwidth=1, relief="solid")
            header.grid(row=0, column=col, sticky="nsew")

        # Cria as linhas da tabela com botões Editar e Excluir na última coluna
        for row in range(1, len(dados) + 1):
            for col in range(len(colunas)):
                if col == len(colunas) - 1:
                    action_frame = ttk.Frame(frame)
                    edit_button = ttk.Button(action_frame, text="Editar", command=lambda r=row: self.editar_callback(dados[r-1]))
                    delete_button = ttk.Button(action_frame, text="Excluir", command=lambda r=row: self.excluir_callback(dados[r-1]))
                    edit_button.pack(side=tk.LEFT)
                    delete_button.pack(side=tk.LEFT)
                    action_frame.grid(row=row, column=col, sticky="nsew")
                else:
                    cell = ttk.Label(frame, text=dados[row-1][col], borderwidth=1, relief="solid")
                    cell.grid(row=row, column=col, sticky="nsew")

        # Configura o peso das colunas e linhas para expandir as células da tabela
        for col in range(len(colunas)):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(len(dados) + 1):
            frame.grid_rowconfigure(row, weight=1)