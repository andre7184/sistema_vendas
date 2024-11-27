import tkinter as tk
from tkinter import ttk

class Grid(tk.Frame):
    def __init__(self, master, colunas, dados, editar_callback, excluir_callback):
        super().__init__(master)
        self.editar_callback = editar_callback
        self.excluir_callback = excluir_callback
        self.n_colunas = colunas
        self.n_dados = dados
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets(self.n_colunas, self.n_dados)

    def create_widgets(self, colunas, dados):
        # Adiciona a coluna 'Ações' às colunas
        colunas.append('Ações')

        # Cria um frame para a tabela
        frame = ttk.Frame(self)
        
        # como alinhar ao topo da janela
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
                    edit_button = ttk.Button(action_frame, text="Editar", command=lambda r=row: self.editar_callback(r))
                    delete_button = ttk.Button(action_frame, text="Excluir", command=lambda r=row: self.excluir_callback(r))
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


    # cria metodo para atualizar a grid
    def update_grid(self):
        self.destroy()
        self.create_widgets(self.n_colunas, self.n_dados)

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
    # Exclui a linha da lista
    print(f"Remover linha {row}")
    # Exclui a linha da lista
    if 0 <= row - 1 < len(data):
        data.pop(row - 1)
        # atualiza a grid
        grid.update_grid()


# Cria a janela principal e a tabela
# Cria a janela principal
root = tk.Tk()

# Define o tamanho da janela (largura x altura)
root.geometry("800x600")
grid = Grid(root, columns, data, editar_callback, excluir_callback)
root.mainloop()