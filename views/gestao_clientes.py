import tkinter as tk
from components.grid import Grid
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

        self.mensagem_titulo = tk.Label(self, text="Gerenciamento de Clientes", fg="blue", font=("Arial", 16))
        self.mensagem_titulo.pack()

        self.mensagem_label = tk.Label(self, text="", fg="red")
        self.mensagem_label.pack()

        self.lista_clientes = Grid(self, colunas, self.dados, self.editar_cliente, self.excluir_cliente)
        
        self.btn_cadastrar_cliente = tk.Button(self, text="Cadastrar Cliente", command=self.cadastrar_cliente)
        self.btn_cadastrar_cliente.pack(pady=10)

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

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def atualizar_lista(self):
        self.clear_frame()
        self.showGrid(self.cliente_controller)

    def mostrar_mensagem(self, mensagem, tipo):
        if tipo == "sucesso":
            self.mensagem_label.config(text=mensagem, fg="green")
        else:
            self.mensagem_label.config(text=mensagem, fg="red")