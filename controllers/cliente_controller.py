import requests
from controllers.models import Cliente

class ClienteController:
    def __init__(self):
        self.api_url = "http://localhost:5000/clientes"
        self.clientes = []

    def cadastrar_cliente(self, nome, cpf, endereco):
        data = {"nome": nome, "cpf": cpf, "endereco": endereco}
        response = requests.post(self.api_url, json=data)
        if response.status_code == 201:
            cliente_data = response.json()
            cliente = Cliente(cliente_data['id'], nome, cpf, endereco)
            self.clientes.append(cliente)
            return cliente_data['id']  # Retornar o ID do cliente criado
        else:
            print(f"Erro ao cadastrar cliente: {response.json()}")
            return None

    def listar_clientes(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            clientes_data = response.json()
            print("Dados recebidos da API:", clientes_data)  # Verificar os dados retornados
            if isinstance(clientes_data, list):
                self.clientes = [Cliente(cliente['id'], cliente['nome'], cliente['cpf'], cliente['endereco']) for cliente in clientes_data]
            else:
                print("Erro: A resposta da API não é uma lista de clientes.")
                self.clientes = []
            return self.clientes
        else:
            print(f"Erro ao listar clientes: {response.json()}")
            return []
    
    def buscar_cliente_por_id(self, id):
        response = requests.get(f"{self.api_url}/{id}")
        if response.status_code == 200:
            cliente_data = response.json()
            return Cliente(cliente_data['id'], cliente_data['nome'], cliente_data['cpf'], cliente_data['endereco'])
        else:
            print(f"Erro ao buscar cliente por ID: {response.json()}")
            return None

    def buscar_cliente_por_nome(self, nome):
        response = requests.get(self.api_url, params={"nome": nome})
        if response.status_code == 200:
            clientes_data = response.json()
            return [Cliente(cliente['id'], cliente['nome'], cliente['cpf'], cliente['endereco']) for cliente in clientes_data]
        else:
            print(f"Erro ao buscar cliente por nome: {response.json()}")
            return []

    def atualizar_cliente(self, id, nome, cpf, endereco):
        data = {"nome": nome, "cpf": cpf, "endereco": endereco}
        response = requests.put(f"{self.api_url}/{id}", json=data)
        if response.status_code == 200:
            cliente = self.buscar_cliente_por_id(id)
            if cliente:
                cliente.set_nome(nome)
                cliente.set_cpf(cpf)
                cliente.set_endereco(endereco)
        else:
            print(f"Erro ao atualizar cliente: {response.json()}")

    def excluir_cliente(self, id):
        response = requests.delete(f"{self.api_url}/{id}")
        if response.status_code == 200:
            self.clientes = [cliente for cliente in self.clientes if cliente.get_id() != id]
        else:
            print(f"Erro ao excluir cliente: {response.json()}")