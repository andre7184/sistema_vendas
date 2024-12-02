from db.models import Usuario
#from db.crud import CRUD

class UsuarioController:
    def __init__(self):
        #self.crud = CRUD()
        self.tabela = "usuarios"
        self.colunas = ["id", "nome", "login", "senha", "tipo"]
        self.usuarios = []
        self.next_id = 1  # Inicializa o próximo ID
        usuarios_teste = [
            {"nome": "Admin", "login": "admin", "senha": "admin123", "tipo": "Administrador"},
            {"nome": "Joao", "login": "joao", "senha": "123", "tipo": "Vendedor"},
            {"nome": "Maria", "login": "maria", "senha": "1425", "tipo": "Vendedor"},
            {"nome": "Andre", "login": "andre", "senha": "123", "tipo": "Vendedor"},
        ]
        for usuario in usuarios_teste:
            self.cadastrar_usuario(usuario["nome"], usuario["login"], usuario["senha"], usuario["tipo"])

    def cadastrar_usuario(self, nome, login, senha, tipo):
        usuario = Usuario(self.next_id, nome, login, senha, tipo)
        self.usuarios.append(usuario)
        self.next_id += 1
        # Descomente as linhas abaixo para usar o banco de dados
        # valores = (nome, cpf, endereco, login, senha, tipo)
        # self.crud.criar(self.tabela, self.colunas[1:], valores)  # Exclui o 'id'
        return usuario

    def listar_usuarios(self):
        # Descomente as linhas abaixo para usar o banco de dados
        # usuarios = self.crud.listar(self.tabela, self.colunas)
        # return [Usuario(*usuario) for usuario in usuarios]
        return self.usuarios

    def buscar_usuario_por_id(self, id):
        # Descomente as linhas abaixo para usar o banco de dados
        # usuario = self.crud.buscar_por_id(self.tabela, self.colunas, "id", id)
        # if usuario:
        #     return Usuario(*usuario)
        return next((usuario for usuario in self.usuarios if usuario.get_id() == id), None)

    def atualizar_usuario(self, id, nome, login, senha, tipo):
        # Descomente as linhas abaixo para usar o banco de dados
        # valores = (nome, cpf, endereco, login, senha, tipo)
        # self.crud.atualizar(self.tabela, self.colunas[1:], valores, "id", id)  # Exclui o 'id'
        usuario = self.buscar_usuario_por_id(id)
        if usuario:
            usuario.set_nome(nome)  # Atualiza o nome
            usuario.set_login(login)  # Atualiza o login
            usuario.set_senha(senha)  # Atualiza a senha
            usuario.set_tipo(tipo)  # Atualiza o tipo

    def excluir_usuario(self, id):
        # Descomente as linhas abaixo para usar o banco de dados
        # self.crud.excluir(self.tabela, "id", id)
        self.usuarios = [usuario for usuario in self.usuarios if usuario.get_id() != id]

    def autenticar_usuario(self, login, senha):
        for usuario in self.usuarios:
            if usuario.get_login() == login and usuario.get_senha() == senha:
                return usuario
        # Descomente as linhas abaixo para usar o banco de dados
        # condicao = "login = %s AND senha = %s"
        # valores = (login, senha)
        # usuario = self.crud.buscar_por_condicao(self.tabela, self.colunas, condicao, valores)
        # if usuario:
        #     return Usuario(*usuario)
        return None