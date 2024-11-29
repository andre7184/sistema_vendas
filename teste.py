import tkinter as tk
from tkinter import ttk

class Grid(tk.Frame):
    def __init__(self, master, colunas, dados, condicao_especial=False):
        super().__init__(master)
        self.condicao_especial = condicao_especial
        self.colunas = colunas  # Inicializa self.colunas
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets(colunas, dados)

    def create_widgets(self, colunas, dados):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Criar a árvore (treeview)
        self.tree = ttk.Treeview(frame, columns=colunas, show='headings')
        for col in colunas:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, anchor=tk.CENTER, width=50)  # Ajustar a largura da coluna ID
            else:
                self.tree.column(col, anchor=tk.CENTER)

        # Adicionar dados à árvore
        for row in dados:
            self.tree.insert('', tk.END, values=row)

        # Adicionar barras de rolagem
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Posicionar a árvore e as barras de rolagem
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Configurar redimensionamento
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def add_row(self, dados):
        self.tree.insert('', tk.END, values=dados)

    def remove_row(self):
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)

# Funções de callback para edição e exclusão
def editar_callback():
    selected_item = grid.tree.selection()[0]
    values = grid.tree.item(selected_item, 'values')
    print(f"Editar: {values}")
    # Aqui você pode adicionar a lógica para editar os dados

def excluir_callback():
    selected_item = grid.tree.selection()[0]
    values = grid.tree.item(selected_item, 'values')
    print(f"Excluir: {values}")
    grid.remove_row()
    # Aqui você pode adicionar a lógica para remover os dados da lista original

# Função para adicionar uma nova linha
def add_new_row():
    new_data = [19, 'Novo', '00000000000', 'Novo Endereço', 'novo', 'comum']
    grid.add_row(new_data)

# Criar a janela principal
root = tk.Tk()
root.title("Tabela com Tkinter")
root.geometry("800x600")

# Criar botões de ação
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

add_btn = tk.Button(button_frame, text="Cadastrar", command=add_new_row)
add_btn.pack(side=tk.LEFT, padx=5, pady=5)

edit_btn = tk.Button(button_frame, text="Editar", state=tk.DISABLED, command=editar_callback)
edit_btn.pack(side=tk.LEFT, padx=5, pady=5)

delete_btn = tk.Button(button_frame, text="Excluir", state=tk.DISABLED, command=excluir_callback)
delete_btn.pack(side=tk.LEFT, padx=5, pady=5)

# Função para ativar/desativar botões
def on_tree_select(event):
    if grid.tree.selection():
        edit_btn.config(state=tk.NORMAL)
        delete_btn.config(state=tk.NORMAL)
    else:
        edit_btn.config(state=tk.DISABLED)
        delete_btn.config(state=tk.DISABLED)

# Dados fornecidos
columns = ['ID', 'Nome', 'CPF', 'Endereço', 'Login', 'Tipo']
data = [
    [1, 'Admin', '00000000000', 'Endereço Admin', 'admin', 'administrador'],
    [2, 'User', '11111111111', 'Endereço User', 'user', 'comum'],
    [3, 'User 2', '22222222222', 'Endereço User 2', 'user2', 'comum'],
    [4, 'User 3', '33333333333', 'Endereço User 3', 'user3', 'comum'],
    [5, 'User 4', '44444444444', 'Endereço User 4', 'user4', 'comum'],
    [6, 'User 5', '55555555555', 'Endereço User 5', 'user5', 'comum'],
    [7, 'User 6', '66666666666', 'Endereço User 6', 'user6', 'comum'],
    [8, 'User 7', '77777777777', 'Endereço User 7', 'user7', 'comum'],
    [9, 'User 8', '88888888888', 'Endereço User 8', 'user8', 'comum'],
    [10, 'User 9', '99999999999', 'Endereço User 9', 'user9', 'comum'],
    [11, 'User 10', '10101010101', 'Endereço User 10', 'user10', 'comum'],
    [12, 'User 11', '11111111111', 'Endereço User 11', 'user11', 'comum'],
    [13, 'User 12', '12121212121', 'Endereço User 12', 'user12', 'comum'],
    [14, 'User 13', '13131313131', 'Endereço User 13', 'user13', 'comum'],
    [15, 'User 14', '14141414141', 'Endereço User 14', 'user14', 'comum'],
    [16, 'User 15', '15151515151', 'Endereço User 15', 'user15', 'comum'],
    [17, 'User 16', '16161616161', 'Endereço User 16', 'user16', 'comum'],
    [18, 'User 17', '17171717171', 'Endereço User 17', 'user17', 'comum'],
    [19, 'User 18', '18181818181', 'Endereço User 18', 'user18', 'comum']
]

# Criar a grid
grid = Grid(root, columns, data)

grid.tree.bind('<<TreeviewSelect>>', on_tree_select)

root.mainloop()