import requests
from controllers.models import Usuario

class UsuarioController:
    def __init__(self):
        self.api_url = "http://localhost:5000/usuarios"
        self.usuarios = []

    def cadastrar_usuario(self, nome, login, senha, tipo):
        senha_hashed = senha
        data = {"nome": nome, "login": login, "senha": senha_hashed, "tipo": tipo}
        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            usuario_data = response.json()
            usuario = Usuario(usuario_data['id'], nome, login, senha_hashed, tipo)
            self.usuarios.append(usuario)
            return usuario
        except requests.exceptions.RequestException as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return None

    def listar_usuarios(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            usuarios_data = response.json()
            self.usuarios = [Usuario(usuario['id'], usuario['nome'], usuario['login'], usuario['senha'], usuario['tipo']) for usuario in usuarios_data]
            return self.usuarios
        except requests.exceptions.RequestException as e:
            print(f"Erro ao listar usuários: {e}")
            return []

    def buscar_usuario_por_id(self, id):
        try:
            response = requests.get(f"{self.api_url}/{id}")
            response.raise_for_status()
            usuario_data = response.json()
            return Usuario(usuario_data['id'], usuario_data['nome'], usuario_data['login'], usuario_data['senha'], usuario_data['tipo'])
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar usuário por ID: {e}")
            return None

    def atualizar_usuario(self, id, nome, login, senha, tipo):
        senha_hashed = senha
        data = {"nome": nome, "login": login, "senha": senha_hashed, "tipo": tipo}
        try:
            response = requests.put(f"{self.api_url}/{id}", json=data)
            response.raise_for_status()
            usuario = self.buscar_usuario_por_id(id)
            if usuario:
                usuario.set_nome(nome)
                usuario.set_login(login)
                usuario.set_senha(senha)
                usuario.set_tipo(tipo)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar usuário: {e}")

    def excluir_usuario(self, id):
        try:
            response = requests.delete(f"{self.api_url}/{id}")
            response.raise_for_status()
            self.usuarios = [usuario for usuario in self.usuarios if usuario.get_id() != id]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao excluir usuário: {e}")

    def autenticar_usuario(self, login, senha):
        senha_hashed = senha
        data = {"login": login, "senha": senha_hashed}
        try:
            response = requests.post(f"{self.api_url}/autenticar", json=data)
            response.raise_for_status()
            usuario_data = response.json()
            return Usuario(usuario_data['id'], usuario_data['nome'], usuario_data['login'], None, usuario_data['tipo'])
        except requests.exceptions.RequestException as e:
            print(f"Erro ao autenticar usuário: {e}")
            return None
