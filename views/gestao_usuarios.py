import tkinter as tk
from components.grid import Grid
from views.cadastro_usuario import CadastroUsuario

class GestaoUsuarios(tk.Frame):
    def __init__(self, master, usuario_controller):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.pack(fill=tk.BOTH, expand=True)
        
        colunas = ["Nome", "CPF", "Endereço", "Login", "Tipo"]
        self.dados = [(usuario.nome, usuario.cpf, usuario.endereco, usuario.login, usuario.tipo) for usuario in usuario_controller.listar_usuarios()]
        
        self.lista_usuarios = Grid(self, colunas, self.dados, self.editar_usuario, self.excluir_usuario)
        
        self.btn_cadastrar_usuario = tk.Button(self, text="Cadastrar Usuário", command=self.cadastrar_usuario)
        self.btn_cadastrar_usuario.pack(pady=10)

    def cadastrar_usuario(self):
        self.clear_frame()
        self.cadastro_usuario_frame = CadastroUsuario(self, self.usuario_controller)
        self.cadastro_usuario_frame.pack()

    def editar_usuario(self, usuario):
        self.clear_frame()
        self.cadastro_usuario_frame = CadastroUsuario(self, self.usuario_controller, usuario)
        self.cadastro_usuario_frame.pack()

    def excluir_usuario(self, usuario):
        self.usuario_controller.excluir_usuario(usuario[1])  # Supondo que o CPF é o identificador único
        self.atualizar_lista()

    def atualizar_lista(self):
        self.dados = [(usuario.nome, usuario.cpf, usuario.endereco, usuario.login, usuario.tipo) for usuario in self.usuario_controller.listar_usuarios()]
        self.lista_usuarios.atualizar_lista(self.dados)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()