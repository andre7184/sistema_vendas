import tkinter as tk
from components.itens import criar_titulo, criar_texto, criar_input, criar_botao, criar_frame, criar_mensagem

class Login(tk.Frame):
    def __init__(self, master, usuario_controller, on_login_success):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.on_login_success = on_login_success
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        self.container = criar_frame(self, "Login", lado=tk.TOP, preencher=tk.BOTH, expandir=True)
        self.container.config(bd=2, relief=tk.RAISED)  # Adiciona uma borda cinza ao redor do menu
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.inner_frame = criar_frame(self.container, "Login", lado=tk.TOP, preencher=tk.BOTH, expandir=True)
        self.inner_frame.config(padx=20, pady=20)  # Adiciona padding interno
        
        criar_titulo(self.inner_frame, "Entre no Sistema", "Login", fonte=("Arial", 16))
        criar_texto(self.inner_frame, "Usuário", "Login", lado=tk.TOP)
        self.entry_login = criar_input(self.inner_frame, "Login", lado=tk.TOP)
        
        criar_texto(self.inner_frame, "Senha", "Login", lado=tk.TOP)
        self.entry_senha = criar_input(self.inner_frame, "Login", estado=tk.NORMAL, lado=tk.TOP)
        self.entry_senha.config(show="*")
        
        self.button_login = criar_botao(self.inner_frame, "Entrar", self.fazer_login, "Login", lado=tk.TOP, padx=5, pady=5)
        self.label_erro = criar_mensagem(self.inner_frame, "", "", tipo="erro")

    def bind_events(self):
        self.entry_login.bind("<Return>", self.on_enter)
        self.entry_senha.bind("<Return>", self.on_enter)
        self.entry_login.bind("<Key>", self.clear_error)
        self.entry_senha.bind("<Key>", self.clear_error)

    def on_enter(self, event):
        self.fazer_login()

    def clear_error(self, event):
        self.label_erro.config(text="")

    def fazer_login(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        usuario = self.usuario_controller.autenticar_usuario(login, senha)
        if usuario:
            self.on_login_success(usuario)
        else:
            self.label_erro.config(text="Login ou senha incorretos")