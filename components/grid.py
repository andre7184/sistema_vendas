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
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        
        # Configurando a largura das colunas
        for coluna in colunas:
            self.tree.column(coluna, width=150, anchor=tk.W)
            self.tree.heading(coluna, text=coluna)
        
        # Adicionando a coluna de ações
        self.tree["columns"] = colunas + ["Ações"]
        self.tree.column("Ações", width=150, anchor=tk.CENTER)
        self.tree.heading("Ações", text="Ações")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.atualizar_lista(dados)

    def atualizar_lista(self, dados):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in dados:
            item_id = self.tree.insert("", tk.END, values=item)
            self.add_action_buttons(item_id)

    def add_action_buttons(self, item_id):
        frame = tk.Frame(self.tree)
        btn_editar = tk.Button(frame, text="Editar", command=lambda: self.editar_callback(self.tree.item(item_id)["values"]))
        btn_excluir = tk.Button(frame, text="Excluir", command=lambda: self.excluir_callback(self.tree.item(item_id)["values"]))
        btn_editar.pack(side=tk.LEFT)
        btn_excluir.pack(side=tk.LEFT)
        self.tree.set(item_id, "Ações", "")
        self.tree.item(item_id, tags=(item_id,))
        self.tree.tag_bind(item_id, "<Button-1>", lambda event, frame=frame: self.show_action_buttons(event, frame, item_id))

    def show_action_buttons(self, event, frame, item_id):
        bbox = self.tree.bbox(item_id, column="Ações")
        if bbox:
            x, y, width, height = bbox
            frame.place(x=x, y=y, width=width, height=height)