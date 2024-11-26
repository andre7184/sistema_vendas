from db.models import Usuario
# from db.connection import get_connection

class UsuarioController:
    def __init__(self):
        self.usuarios = []
        admin = Usuario("Admin", "00000000000", "Endereço Admin", "admin", "admin123", "administrador")
        self.usuarios.append(admin)

    def cadastrar_usuario(self, nome, cpf, endereco, login, senha, tipo):
        usuario = Usuario(nome, cpf, endereco, login, senha, tipo)
        self.usuarios.append(usuario)
        # Descomente as linhas abaixo para usar o banco de dados
        # conn = get_connection()
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO usuarios (nome, cpf, endereco, login, senha, tipo) VALUES (%s, %s, %s, %s, %s, %s)",
        #                (usuario.nome, usuario.cpf, usuario.endereco, usuario.login, usuario.senha, usuario.tipo))
        # conn.commit()
        # cursor.close()
        # conn.close()
        return usuario

    def listar_usuarios(self):
        # Descomente as linhas abaixo para usar o banco de dados
        # conn = get_connection()
        # cursor = conn.cursor()
        # cursor.execute("SELECT nome, cpf, endereco, login, senha, tipo FROM usuarios")
        # usuarios = cursor.fetchall()
        # cursor.close()
        # conn.close()
        # return [Usuario(nome, cpf, endereco, login, senha, tipo) for nome, cpf, endereco, login, senha, tipo in usuarios]
        return self.usuarios

    def autenticar_usuario(self, login, senha):
        for usuario in self.usuarios:
            if usuario.login == login and usuario.senha == senha:
                return usuario
        # Descomente as linhas abaixo para usar o banco de dados
        # conn = get_connection()
        # cursor = conn.cursor()
        # cursor.execute("SELECT nome, cpf, endereco, login, senha, tipo FROM usuarios WHERE login = %s AND senha = %s", (login, senha))
        # usuario = cursor.fetchone()
        # cursor.close()
        # conn.close()
        # if usuario:
        #     return Usuario(*usuario)
        return None