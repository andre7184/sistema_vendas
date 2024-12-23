import tkinter as tk
from components.itens import criar_titulo, criar_mensagem, criar_botao, criar_frame
from components.cores import obter_cor
from components.grid import Grid
from views.cadastro_usuario import CadastroUsuario

class GestaoUsuarios(tk.Frame):
    def __init__(self, master, usuario_controller):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.showGrid(usuario_controller)

    def showGrid(self, usuario_controller):
        self.pack(fill=tk.BOTH, expand=True)
        colunas = ["ID", "Nome", "Login", "Tipo"]
        self.dados = [(usuario.get_id(), usuario.get_nome(), usuario.get_login(), usuario.get_tipo()) for usuario in usuario_controller.listar_usuarios()]
        self.titulo = criar_titulo(self, "Gerenciamento de Usuários", "GestaoUsuarios", fonte=("Arial", 16), pady=5)
        self.mensagem_label = criar_mensagem(self, "GestaoUsuarios", "", tipo="sucesso")
        self.button_frame = criar_frame(self, "GestaoUsuarios", lado=tk.TOP)
        self.btn_cadastrar_usuario = criar_botao(self.button_frame, "Cadastrar Usuário", self.cadastrar_usuario, "GestaoUsuarios", altura=1, lado=tk.LEFT, padx=5, pady=5)
        self.btn_editar_usuario = criar_botao(self.button_frame, "Editar Usuário", self.editar_usuario_selecionado, "GestaoUsuarios", altura=1, lado=tk.LEFT, padx=5, pady=5, estado=tk.DISABLED)
        self.btn_excluir_usuario = criar_botao(self.button_frame, "Excluir Usuário", self.excluir_usuario_selecionado, "GestaoUsuarios", altura=1, lado=tk.LEFT, padx=5, pady=5, estado=tk.DISABLED)
        self.lista_usuarios = Grid(self, colunas, self.dados)
        self.lista_usuarios.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

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
        self.usuario_controller.excluir_usuario(usuario[0])
        self.atualizar_lista()

    def editar_usuario_selecionado(self):
        selected_item = self.lista_usuarios.tree.selection()[0]
        usuario_id = self.lista_usuarios.tree.item(selected_item)['values'][0]
        usuario_obj = self.usuario_controller.buscar_usuario_por_id(usuario_id)
        self.editar_usuario((usuario_obj.get_id(), usuario_obj.get_nome(), usuario_obj.get_login(), usuario_obj.get_tipo()))

    def excluir_usuario_selecionado(self):
        selected_item = self.lista_usuarios.tree.selection()[0]
        usuario_id = self.lista_usuarios.tree.item(selected_item)['values'][0]
        self.excluir_usuario((usuario_id,))

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def atualizar_lista(self):
        self.clear_frame()
        self.showGrid(self.usuario_controller)

    def mostrar_mensagem(self, mensagem, tipo):
        self.mensagem_label.config(text=mensagem, fg=obter_cor("GestaoUsuarios", tipo))

    def on_tree_select(self, event):
        if self.lista_usuarios.tree.selection():
            self.btn_editar_usuario.config(state=tk.NORMAL)
            self.btn_excluir_usuario.config(state=tk.NORMAL)
        else:
            self.btn_editar_usuario.config(state=tk.DISABLED)
            self.btn_excluir_usuario.config(state=tk.DISABLED)