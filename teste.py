import tkinter as tk
from tkinter import ttk

class Grid(tk.Frame):
    def __init__(self, master, colunas, dados, editar_callback, excluir_callback, condicao_especial=False):
        super().__init__(master)
        self.editar_callback = editar_callback
        self.excluir_callback = excluir_callback
        self.condicao_especial = condicao_especial
        self.colunas = colunas
        self.grid_widgets = []
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets(colunas, dados)

    def create_widgets(self, colunas, dados):
        colunas.append('Ações')

        # Cria um Canvas e uma Scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Ajuste para expandir horizontalmente
        self.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

        # Adiciona o frame ao scrollable_frame
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill=tk.X, expand=True, padx=10, pady=10, anchor='n')

        for col in range(len(colunas)):
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

        # Configura a expansão horizontal das colunas
        for col in range(len(colunas)):
            frame.grid_columnconfigure(col, weight=1)
        for row in range(len(dados) + 1):
            frame.grid_rowconfigure(row, weight=1)

    def add_row(self, dados):
        frame = self.winfo_children()[0].winfo_children()[0].winfo_children()[0]  # Obtém o frame principal
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
        frame = self.winfo_children()[0].winfo_children()[0].winfo_children()[0]  # Obtém o frame principal
        row_widgets = []
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget("text") == dados[0]:  # Verifica se a linha corresponde ao ID do produto
                row = widget.grid_info()["row"]
                row_widgets = [w for w in frame.winfo_children() if w.grid_info()["row"] == row]
                break
        for widget in row_widgets:
            widget.destroy()
            self.grid_widgets.remove(widget)

# Define as colunas e os dados
columns = ['Nome', 'CPF', 'Endereço', 'Login', 'Tipo']
data = [
    ('Admin', '00000000000', 'Endereço Admin', 'admin', 'administrador'),
    ('User', '11111111111', 'Endereço User', 'user', 'comum'),
    ('User 2', '22222222222', 'Endereço User 2', 'user2', 'comum'),
    ('User 3', '33333333333', 'Endereço User 3', 'user3', 'comum'),
    ('User 4', '44444444444', 'Endereço User 4', 'user4', 'comum'),
    ('User 5', '55555555555', 'Endereço User 5', 'user5', 'comum'),
    ('User 6', '66666666666', 'Endereço User 6', 'user6', 'comum'),
    ('User 7', '77777777777', 'Endereço User 7', 'user7', 'comum'),
    ('User 8', '88888888888', 'Endereço User 8', 'user8', 'comum'),
    ('User 9', '99999999999', 'Endereço User 9', 'user9', 'comum'),
    ('User 10', '10101010101', 'Endereço User 10', 'user10', 'comum'),
    ('User 11', '11111111111', 'Endereço User 11', 'user11', 'comum'),
    ('User 12', '12121212121', 'Endereço User 12', 'user12', 'comum'),
    ('User 13', '13131313131', 'Endereço User 13', 'user13', 'comum'),
    ('User 14', '14141414141', 'Endereço User 14', 'user14', 'comum'),
    ('User 15', '15151515151', 'Endereço User 15', 'user15', 'comum'),
    ('User 16', '16161616161', 'Endereço User 16', 'user16', 'comum'),
    ('User 17', '17171717171', 'Endereço User 17', 'user17', 'comum'),
    ('User 18', '18181818181', 'Endereço User 18', 'user18', 'comum')
]

# Funções de callback para os botões Editar e Excluir
def editar_callback(row):
    print(f"Editar linha {row}")

def excluir_callback(row):
    print(f"Remover linha {row}")
    if 0 <= row - 1 < len(data):
        data.pop(row - 1)
        grid.update_grid()

# Cria a janela principal
root = tk.Tk()
root.geometry("800x600")
grid = Grid(root, columns, data, editar_callback, excluir_callback)
root.mainloop()