from db.models import Cliente
#from db.crud import CRUD

class ClienteController:
    def __init__(self):
        #self.crud = CRUD()
        self.tabela = "clientes"
        self.colunas = ["id", "nome", "cpf", "endereco"]
        self.clientes = []
        self.next_id = 1  # Inicializa o próximo ID
        clientes_teste = [
            {"nome": "Cliente A", "cpf": "111.111.111-11", "endereco": "Endereço A"},
            {"nome": "Cliente B", "cpf": "222.222.222-22", "endereco": "Endereço B"},
            {"nome": "Cliente C", "cpf": "333.333.333-33", "endereco": "Endereço C"},
            {"nome": "Cliente D", "cpf": "444.444.444-44", "endereco": "Endereço D"}
        ]
        for cliente in clientes_teste:
            self.cadastrar_cliente(cliente["nome"], cliente["cpf"], cliente["endereco"])

    def cadastrar_cliente(self, nome, cpf, endereco):
        cliente = Cliente(self.next_id, nome, cpf, endereco)
        self.clientes.append(cliente)
        self.next_id += 1
        # Descomente as linhas abaixo para usar o banco de dados
        # valores = (nome, cpf, endereco)
        # self.crud.criar(self.tabela, self.colunas[1:], valores)  # Exclui o 'id'
        return cliente

    def listar_clientes(self):
        # Descomente as linhas abaixo para usar o banco de dados
        # clientes = self.crud.listar(self.tabela, self.colunas)
        # return [Cliente(*cliente) for cliente in clientes]
        return self.clientes

    def buscar_cliente_por_id(self, id):
        # Descomente as linhas abaixo para usar o banco de dados
        # cliente = self.crud.buscar_por_id(self.tabela, self.colunas, "id", id)
        # if cliente:
        #     return Cliente(*cliente)
        return next((cliente for cliente in self.clientes if cliente.get_id() == id), None)

    def buscar_cliente_por_nome(self, nome):
        # Descomente as linhas abaixo para usar o banco de dados
        # condicao = "nome LIKE %s"
        # valores = (f"%{nome}%",)
        # clientes = self.crud.buscar_por_condicao(self.tabela, self.colunas, condicao, valores)
        # return [Cliente(*cliente) for cliente in clientes]
        return [cliente for cliente in self.clientes if nome.lower() in cliente.get_nome().lower()]

    def atualizar_cliente(self, id, nome, cpf, endereco):
        print(id, nome, cpf, endereco)
        # Descomente as linhas abaixo para usar o banco de dados
        # valores = (nome, cpf, endereco)
        # self.crud.atualizar(self.tabela, self.colunas[1:], valores, "id", id)  # Exclui o 'id'
        cliente = self.buscar_cliente_por_id(id)
        if cliente:
            cliente.set_nome(nome)  # Atualiza o nome
            cliente.set_cpf(cpf)  # Atualiza o cpf
            cliente.set_endereco(endereco)  # Atualiza o endereco

    def excluir_cliente(self, id):
        # Descomente as linhas abaixo para usar o banco de dados
        # self.crud.excluir(self.tabela, "id", id)
        self.clientes = [cliente for cliente in self.clientes if cliente.get_id() != id]