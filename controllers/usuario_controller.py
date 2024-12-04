import requests
from controllers.models import Usuario

class UsuarioController:
    def __init__(self):
        self.api_url = "http://localhost:5000/usuarios"
        self.usuarios = []
        self.next_id = 1  # Inicializa o próximo ID

    def cadastrar_usuario(self, nome, login, senha, tipo):
        data = {"nome": nome, "login": login, "senha": senha, "tipo": tipo}
        response = requests.post(self.api_url, json=data)
        if response.status_code == 201:
            usuario_data = response.json()
            usuario = Usuario(usuario_data['id'], nome, login, senha, tipo)
            self.usuarios.append(usuario)
            return usuario
        else:
            print(f"Erro ao cadastrar usuário: {response.json()}")
            return None

    def listar_usuarios(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            usuarios_data = response.json()
            self.usuarios = [Usuario(usuario['id'], usuario['nome'], usuario['login'], usuario['senha'], usuario['tipo']) for usuario in usuarios_data]
            return self.usuarios
        else:
            print(f"Erro ao listar usuários: {response.json()}")
            return []

    def buscar_usuario_por_id(self, id):
        response = requests.get(f"{self.api_url}/{id}")
        if response.status_code == 200:
            usuario_data = response.json()
            return Usuario(usuario_data['id'], usuario_data['nome'], usuario_data['login'], usuario_data['senha'], usuario_data['tipo'])
        else:
            print(f"Erro ao buscar usuário por ID: {response.json()}")
            return None

    def atualizar_usuario(self, id, nome, login, senha, tipo):
        data = {"nome": nome, "login": login, "senha": senha, "tipo": tipo}
        response = requests.put(f"{self.api_url}/{id}", json=data)
        if response.status_code == 200:
            usuario = self.buscar_usuario_por_id(id)
            if usuario:
                usuario.set_nome(nome)
                usuario.set_login(login)
                usuario.set_senha(senha)
                usuario.set_tipo(tipo)
        else:
            print(f"Erro ao atualizar usuário: {response.json()}")

    def excluir_usuario(self, id):
        response = requests.delete(f"{self.api_url}/{id}")
        if response.status_code == 200:
            self.usuarios = [usuario for usuario in self.usuarios if usuario.get_id() != id]
        else:
            print(f"Erro ao excluir usuário: {response.json()}")

    def autenticar_usuario(self, login, senha):
        response = requests.get(self.api_url, params={"login": login, "senha": senha})
        if response.status_code == 200:
            usuario_data = response.json()
            return Usuario(usuario_data['id'], usuario_data['nome'], usuario_data['login'], usuario_data['senha'], usuario_data['tipo'])
        else:
            print(f"Erro ao autenticar usuário: {response.json()}")
            return None