import tkinter as tk
from tkinter import messagebox

class Login(tk.Frame):
    def __init__(self, master, usuario_controller, on_login_success):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.on_login_success = on_login_success
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label_login = tk.Label(self, text="Login")
        self.label_login.pack()
        self.entry_login = tk.Entry(self)
        self.entry_login.pack()

        self.label_senha = tk.Label(self, text="Senha")
        self.label_senha.pack()
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack()

        self.button_login = tk.Button(self, text="Entrar", command=self.fazer_login)
        self.button_login.pack()

    def fazer_login(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        usuario = self.usuario_controller.autenticar_usuario(login, senha)
        print(usuario)
        if usuario:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Erro", "Login ou senha incorretos")