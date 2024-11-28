import tkinter as tk
from components.grid import Grid
from views.cadastro_usuario import CadastroUsuario

class GestaoUsuarios(tk.Frame):
    def __init__(self, master, usuario_controller):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.showGrid(usuario_controller)
        
    def showGrid(self,usuario_controller):
        self.pack(fill=tk.BOTH, expand=True)
        colunas = ["ID", "Nome", "Login", "Tipo"]
        self.dados = [(usuario.id, usuario.nome, usuario.login, usuario.tipo) for usuario in usuario_controller.listar_usuarios()]

        self.mensagem_titulo = tk.Label(self, text="Gerenciamento de Usuários", fg="blue", font=("Arial", 16))
        self.mensagem_titulo.pack()

        self.mensagem_label = tk.Label(self, text="", fg="red")
        self.mensagem_label.pack()

        self.lista_usuarios = Grid(self, colunas, self.dados, self.editar_usuario, self.excluir_usuario)
        
        self.btn_cadastrar_usuario = tk.Button(self, text="Cadastrar Usuário", command=self.cadastrar_usuario)
        self.btn_cadastrar_usuario.pack(pady=10)

    def cadastrar_usuario(self):
        self.clear_frame()
        self.cadastro_usuario_frame = CadastroUsuario(self, self.usuario_controller)
        self.cadastro_usuario_frame.pack()

    def editar_usuario(self, usuario):
        self.clear_frame()
        usuario_obj = self.usuario_controller.buscar_usuario_por_id(usuario[0])
        self.cadastro_usuario_frame = CadastroUsuario(self, self.usuario_controller, usuario_obj)
        self.cadastro_usuario_frame.pack()

    def excluir_usuario(self, usuario):
        self.usuario_controller.excluir_usuario(usuario[0])  # Usando o ID para exclusão
        self.atualizar_lista()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def atualizar_lista(self):
        print("Atualizando lista...")
        self.clear_frame()
        self.showGrid(self.usuario_controller)

    def mostrar_mensagem(self, mensagem, tipo):
        print(mensagem)
        if tipo == "sucesso":
            self.mensagem_label.config(text=mensagem, fg="green")
        else:
            self.mensagem_label.config(text=mensagem, fg="red")