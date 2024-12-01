import tkinter as tk
from views.cadastro_usuario import CadastroUsuario
from views.cadastro_produto import CadastroProduto
from views.gestao_usuarios import GestaoUsuarios
from views.gestao_produtos import GestaoProdutos
from views.realizacao_vendas import RealizacaoVendas
from views.relatorio_vendas import RelatorioVendas
from views.login import Login
from views.gestao_clientes import GestaoClientes  # Nova importação
from controllers.usuario_controller import UsuarioController
from controllers.produto_controller import ProdutoController
from controllers.venda_controller import VendaController
from controllers.relatorio_controller import RelatorioController
from controllers.cliente_controller import ClienteController  # Nova importação
from components.itens import criar_frame_com_scroll, criar_titulo, criar_texto, criar_frame
from components.cores import obter_cor

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Vendas")
        self.geometry("800x600")
        self.pack_propagate(False)
        self.usuario_controller = UsuarioController()
        self.produto_controller = ProdutoController()
        self.venda_controller = VendaController()
        self.relatorio_controller = RelatorioController()
        self.cliente_controller = ClienteController()  # Inicialização do ClienteController
        self.current_user = None

        self.show_login()

    def show_login(self):
        self.clear_frame()
        self.login_frame = Login(self, self.usuario_controller, self.on_login_success)
        self.login_frame.pack()

    def on_login_success(self, user):
        self.current_user = user
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        self.menu = tk.Menu(self)
        self.config(menu=self.menu, bg=obter_cor("MainApp", "fundo"))

        self.menu_usuarios = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Usuários", menu=self.menu_usuarios)
        self.menu_usuarios.add_command(label="Gerenciamento de Usuários", command=self.show_gestao_usuarios)

        self.menu_produtos = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Produtos", menu=self.menu_produtos)
        self.menu_produtos.add_command(label="Gerenciamento de Produtos", command=self.show_gestao_produtos)

        self.menu_vendas = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Vendas", menu=self.menu_vendas)
        self.menu_vendas.add_command(label="Realização de Vendas", command=self.show_realizacao_vendas)

        self.menu_relatorios = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Relatórios", menu=self.menu_relatorios)
        self.menu_relatorios.add_command(label="Relatório de Vendas", command=self.show_relatorio_vendas)

        self.menu_clientes = tk.Menu(self.menu, tearoff=0)  # Novo menu para clientes
        self.menu.add_cascade(label="Clientes", menu=self.menu_clientes)
        self.menu_clientes.add_command(label="Gerenciamento de Clientes", command=self.show_gestao_clientes)

        self.menu.add_command(label="Sair", command=self.sair)

        criar_titulo(self, f"Bem-vindo, {self.current_user.nome}!", "MainApp", fonte=("Arial", 18))

    def sair(self):
        self.current_user = None
        self.menu.delete(0, tk.END)
        self.show_login()

    def show_gestao_usuarios(self):
        self.clear_frame()
        self.gestao_usuarios_frame = GestaoUsuarios(self, self.usuario_controller)
        self.gestao_usuarios_frame.pack()

    def show_gestao_produtos(self):
        self.clear_frame()
        self.gestao_produtos_frame = GestaoProdutos(self, self.produto_controller)
        self.gestao_produtos_frame.pack()

    def show_realizacao_vendas(self):
        self.clear_frame()
        main_frame, second_frame = criar_frame_com_scroll(self)
        self.realizacao_vendas_frame = RealizacaoVendas(self, second_frame, self.venda_controller, self.produto_controller, self.cliente_controller)
        self.realizacao_vendas_frame.pack()

    def show_relatorio_vendas(self):
        self.clear_frame()
        self.relatorio_vendas_frame = RelatorioVendas(self, self.relatorio_controller)
        self.relatorio_vendas_frame.pack()

    def show_gestao_clientes(self):  # Novo método para exibir a gestão de clientes
        self.clear_frame()
        self.gestao_clientes_frame = GestaoClientes(self, self.cliente_controller)
        self.gestao_clientes_frame.pack()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    app = App()
    app.mainloop()