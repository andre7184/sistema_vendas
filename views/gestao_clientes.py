import tkinter as tk
from components.cores import obter_cor
from components.grid import Grid
from components.itens import criar_botao, criar_frame, criar_mensagem, criar_titulo
from views.cadastro_cliente import CadastroCliente

class GestaoClientes(tk.Frame):
    def __init__(self, master, cliente_controller):
        super().__init__(master)
        self.cliente_controller = cliente_controller
        self.showGrid(cliente_controller)
        
    def showGrid(self, cliente_controller):
        self.pack(fill=tk.BOTH, expand=True)
        colunas = ["ID", "Nome", "CPF", "Endereço"]
        self.dados = [(cliente.id, cliente.nome, cliente.cpf, cliente.endereco) for cliente in cliente_controller.listar_clientes()]
        self.titulo = criar_titulo(self, "Gerenciamento de Cliente", "GestaoClientes", fonte=("Arial", 16), pady=5)
        self.mensagem_label = criar_mensagem(self, "GestaoClientes", "", tipo="sucesso")
        self.button_frame = criar_frame(self, "GestaoClientes", lado=tk.TOP)
        self.btn_cadastrar_cliente = criar_botao(self.button_frame, "Cadastrar Cliente", self.cadastrar_cliente, "GestaoClientes", altura=1, lado=tk.LEFT, padx=5, pady=5)
        self.btn_editar_cliente = criar_botao(self.button_frame, "Editar Cliente", self.editar_cliente_selecionado, "GestaoClientes", altura=1, lado=tk.LEFT, padx=5, pady=5, estado=tk.DISABLED)
        self.btn_excluir_cliente = criar_botao(self.button_frame, "Excluir Cliente", self.excluir_cliente_selecionado, "GestaoClientes", altura=1, lado=tk.LEFT, padx=5, pady=5, estado=tk.DISABLED)
        self.lista_clientes = Grid(self, colunas, self.dados)
        self.lista_clientes.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def cadastrar_cliente(self):
        self.clear_frame()
        self.cadastro_cliente_frame = CadastroCliente(self, self.cliente_controller)
        self.cadastro_cliente_frame.pack()

    def editar_cliente(self, cliente):
        self.clear_frame()
        cliente_obj = self.cliente_controller.buscar_cliente_por_id(cliente[0])
        self.cadastro_cliente_frame = CadastroCliente(self, self.cliente_controller, cliente_obj)
        self.cadastro_cliente_frame.pack()

    def excluir_cliente(self, cliente):
        self.cliente_controller.excluir_cliente(cliente[0])  # Usando o ID para exclusão
        self.atualizar_lista()

    def editar_cliente_selecionado(self):
        selected_item = self.lista_clientes.tree.selection()[0]
        cliente_id = self.lista_clientes.tree.item(selected_item)['values'][0]
        cliente_obj = self.cliente_controller.buscar_cliente_por_id(cliente_id)
        self.editar_cliente((cliente_obj.id, cliente_obj.nome, cliente_obj.cpf, cliente_obj.endereco))

    def excluir_cliente_selecionado(self):
        selected_item = self.lista_clientes.tree.selection()[0]
        cliente_id = self.lista_clientes.tree.item(selected_item)['values'][0]
        self.excluir_cliente((cliente_id,))

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def atualizar_lista(self):
        self.clear_frame()
        self.showGrid(self.cliente_controller)

    def mostrar_mensagem(self, mensagem, tipo):
        self.mensagem_label.config(text=mensagem, fg=obter_cor("GestaoUsuarios", tipo))

    def on_tree_select(self, event):
        if self.lista_clientes.tree.selection():
            self.btn_editar_cliente.config(state=tk.NORMAL)
            self.btn_excluir_cliente.config(state=tk.NORMAL)
        else:
            self.btn_editar_cliente.config(state=tk.DISABLED)
            self.btn_excluir_cliente.config(state=tk.DISABLED)