import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

def adjust_column_width(tree):
    tree.update_idletasks()  # Atualiza a interface para garantir que o conteúdo seja renderizado
    for col in tree['columns']:
        max_width = tkFont.Font().measure(tree.heading(col)['text'])
        for item in tree.get_children():
            cell_text = tree.set(item, col)
            cell_width = tkFont.Font().measure(cell_text)
            if cell_width > max_width:
                max_width = cell_width
        tree.column(col, width=max_width)

root = tk.Tk()
root.title('Treeview demo')

columns = ('first_name', 'last_name', 'email')
tree = ttk.Treeview(root, columns=columns, show='headings')

tree.heading('first_name', text='First Name')
tree.heading('last_name', text='Last Name')
tree.heading('email', text='Email')

# Adiciona dados de exemplo
contacts = [('John', 'Doe', 'john.doe@example.com'),
            ('Jane', 'Smith', 'jane.smith@example.com'),
            ('Emily', 'Jones', 'emily.jones@example.com')]

for contact in contacts:
    tree.insert('', tk.END, values=contact)

tree.pack(fill=tk.BOTH, expand=True)

# Ajusta a largura das colunas
adjust_column_width(tree)

root.mainloop()