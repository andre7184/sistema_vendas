import tkinter as tk
from components.formulario_cadastro import FormularioCadastro

class CadastroUsuario(tk.Frame):
    def __init__(self, master, usuario_controller, usuario=None):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.usuario = usuario
        campos = {
            "Nome": {"tipo": "entry"},
            "Login": {"tipo": "entry"},
            "Senha": {"tipo": "password"},
            "Tipo": {"tipo": "select", "options": ["Administrador", "Vendedor"]}
        }
        
        self.formulario = FormularioCadastro(self, campos, self.salvar_usuario)
        
        if usuario:
            self.preencher_dados(usuario)

    def preencher_dados(self, usuario):
        self.formulario.set_dados({
            "Nome": usuario.nome,
            "Login": usuario.login,
            "Senha": usuario.senha,
            "Tipo": usuario.tipo
        })

    def salvar_usuario(self, dados):
        nome = dados["Nome"]
        login = dados["Login"]
        senha = dados["Senha"]
        tipo = dados["Tipo"]
        
        try:
            if self.usuario:
                self.usuario_controller.atualizar_usuario(self.usuario.id, nome, login, senha, tipo)
                mensagem = "Usuário atualizado com sucesso!"
            else:
                self.usuario_controller.cadastrar_usuario(nome, login, senha, tipo)
                mensagem = "Usuário cadastrado com sucesso!"
            self.master.atualizar_lista()
            self.master.mostrar_mensagem(mensagem, "sucesso")
        except Exception as e:
            mensagem = f"Erro ao salvar usuário: {str(e)}"
            self.formulario.mostrar_mensagem(mensagem, "erro")