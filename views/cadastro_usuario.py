import tkinter as tk
from components.formulario_cadastro import FormularioCadastro

class CadastroUsuario(tk.Frame):
    def __init__(self, master, usuario_controller, usuario=None):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.usuario = usuario
        campos = ["Nome", "CPF", "Endereço", "Login", "Senha", "Tipo"]
        
        self.formulario = FormularioCadastro(self, campos, self.salvar_usuario)
        
        if usuario:
            self.preencher_dados(usuario)

    def preencher_dados(self, usuario):
        self.formulario.set_dados({
            "Nome": usuario.nome,
            "CPF": usuario.cpf,
            "Endereço": usuario.endereco,
            "Login": usuario.login,
            "Senha": usuario.senha,
            "Tipo": usuario.tipo
        })

    def salvar_usuario(self, dados):
        nome = dados["Nome"]
        cpf = dados["CPF"]
        endereco = dados["Endereço"]
        login = dados["Login"]
        senha = dados["Senha"]
        tipo = dados["Tipo"]
        
        if self.usuario:
            # Atualizar o usuário existente
            self.usuario_controller.atualizar_usuario(self.usuario.id, nome, cpf, endereco, login, senha, tipo)
        else:
            # Cadastrar um novo usuário
            self.usuario_controller.cadastrar_usuario(nome, cpf, endereco, login, senha, tipo)