import tkinter as tk
from tkinter import ttk

class Grid(tk.Frame):
    def __init__(self, master, colunas, dados, editar_callback, excluir_callback, condicao_especial=False):
        super().__init__(master)
        self.editar_callback = editar_callback
        self.excluir_callback = excluir_callback
        self.condicao_especial = condicao_especial
        self.colunas = colunas  # Inicializa self.colunas
        self.grid_widgets = []  # Lista para armazenar widgets da grid
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets(colunas, dados)

    def create_widgets(self, colunas, dados):
        colunas.append('Ações')

        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, expand=True, padx=10, pady=10, anchor='n')

        for col in range(len(colunas)):
            # configurar as colunas com o nome das colunas em negrito
            header = ttk.Label(frame, text=colunas[col], borderwidth=1, relief="solid", font=("Arial", 10, "bold"))
            header.grid(row=0, column=col, sticky="nsew")
            self.grid_widgets.append(header)

        for row in range(1, len(dados) + 1):
            for col in range(len(colunas)):
                if col == len(colunas) - 1:
                    action_frame = ttk.Frame(frame)
                    if not self.condicao_especial:
                        edit_button = ttk.Button(action_frame, text="Editar", command=lambda r=row: self.editar_callback(dados[row-1]))
                        edit_button.pack(side=tk.LEFT)
                    
                    delete_button = ttk.Button(action_frame, text="Excluir", command=lambda r=row: self.excluir_callback(dados[row-1]))
                    delete_button.pack(side=tk.LEFT)
                    action_frame.grid(row=row, column=col, sticky="nsew")
                    self.grid_widgets.append(action_frame)
                elif self.condicao_especial and colunas[col] in ["Quantidade", "Desconto"]:
                    entry = tk.Entry(frame)
                    entry.insert(0, dados[row-1][col])
                    entry.grid(row=row, column=col, sticky="nsew")
                    self.grid_widgets.append(entry)
                else:
                    cell = ttk.Label(frame, text=dados[row-1][col], borderwidth=1, relief="solid")
                    cell.grid(row=row, column=col, sticky="nsew")
                    self.grid_widgets.append(cell)

        for col in range(len(colunas)):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(len(dados) + 1):
            frame.grid_rowconfigure(row, weight=1)

    def add_row(self, dados):
        frame = self.winfo_children()[0]  # Obtém o frame principal
        row = len(self.grid_widgets) // len(self.colunas)  # Calcula a próxima linha
        for col in range(len(self.colunas)):
            if col == len(self.colunas) - 1:
                action_frame = ttk.Frame(frame)
                if not self.condicao_especial:
                    edit_button = ttk.Button(action_frame, text="Editar", command=lambda r=row: self.editar_callback(dados))
                    edit_button.pack(side=tk.LEFT)

                delete_button = ttk.Button(action_frame, text="Excluir", command=lambda r=row: self.excluir_callback(dados))
                delete_button.pack(side=tk.LEFT)
                action_frame.grid(row=row, column=col, sticky="nsew")
                self.grid_widgets.append(action_frame)
            elif self.condicao_especial and self.colunas[col] in ["Quantidade", "Desconto"]:
                entry = tk.Entry(frame)
                entry.insert(0, dados[col])
                entry.grid(row=row, column=col, sticky="nsew")
                self.grid_widgets.append(entry)
            else:
                cell = ttk.Label(frame, text=dados[col], borderwidth=1, relief="solid")
                cell.grid(row=row, column=col, sticky="nsew")
                self.grid_widgets.append(cell)

    def remove_row(self, dados):
        print(dados)
        frame = self.winfo_children()[0]  # Obtém o frame principal
        row_widgets = []
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("text") == dados[0]:  # Verifica se a linha corresponde ao ID do produto
                row = widget.grid_info()["row"]
                row_widgets = [w for w in frame.winfo_children() if w.grid_info()["row"] == row]
                break
        for widget in row_widgets:
            widget.destroy()
            self.grid_widgets.remove(widget)