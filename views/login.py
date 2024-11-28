import tkinter as tk

class Login(tk.Frame):
    def __init__(self, master, usuario_controller, on_login_success):
        super().__init__(master)
        self.usuario_controller = usuario_controller
        self.on_login_success = on_login_success
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        self.container = tk.Frame(self, bd=2, relief=tk.RAISED, bg="#D3D3D3")  # Adiciona uma borda cinza ao redor do menu
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.inner_frame = tk.Frame(self.container, padx=20, pady=20)  # Adiciona padding interno
        self.inner_frame.pack(fill=tk.BOTH, expand=True)

        self.label_titulo = tk.Label(self.inner_frame, text="Entre no Sistema", fg="blue", font=("Arial", 16))
        self.label_titulo.pack()

        self.label_login = tk.Label(self.inner_frame, text="Usuário")
        self.label_login.pack(pady=5)
        self.entry_login = tk.Entry(self.inner_frame)
        self.entry_login.pack(pady=5)

        self.label_senha = tk.Label(self.inner_frame, text="Senha")
        self.label_senha.pack(pady=5)
        self.entry_senha = tk.Entry(self.inner_frame, show="*")
        self.entry_senha.pack(pady=5)

        self.button_login = tk.Button(self.inner_frame, text="Entrar", command=self.fazer_login)
        self.button_login.pack(pady=10)

        self.label_erro = tk.Label(self.inner_frame, text="", fg="red")
        self.label_erro.pack(pady=5)

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
        print(usuario)
        if usuario:
            self.on_login_success(usuario)
        else:
            self.label_erro.config(text="Login ou senha incorretos")