import requests
from controllers.models import Venda

class VendaController:
    def __init__(self):
        self.api_url = "http://localhost:5000/vendas"
        self.vendas = []
        self.next_id = 1  # Inicializa o próximo ID

    def cadastrar_venda(self, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas, itens):
        data = {
            "cliente_id": cliente_id,
            "vendedor_id": vendedor_id,
            "data_venda": data_venda,
            "forma_pagamento": forma_pagamento,
            "quantidade_parcelas": quantidade_parcelas,
            "itens": itens
        }
        response = requests.post(self.api_url, json=data)
        if response.status_code == 201:
            venda_data = response.json()
            venda = Venda(venda_data['venda_id'], cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas)
            for item in venda_data['itens']:
                venda.adicionar_item(item['produto_id'], item['quantidade'], item['valor_unitario'])
            self.vendas.append(venda)
            return venda
        else:
            print(f"Erro ao cadastrar venda: {response.json()}")
            return None
        
    def registrar_venda(self, venda):
        itens = [
            {"produto_id": item['id'], "quantidade": item['quantidade'], "valor_unitario": item['valor_unitario']}
            for item in venda['produtos']
        ]
        return self.cadastrar_venda(
            venda['cliente'].get_id(),
            venda['vendedor'].get_id(),
            venda['data_venda'],
            venda['forma_pagamento'],
            venda['quantidade_parcelas'],
            itens
        )

    def listar_vendas(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            vendas_data = response.json()
            print("Dados recebidos da API:", vendas_data)
            self.vendas = [Venda(venda[0], venda[1], venda[2], venda[3], venda[4], venda[5]) for venda in vendas_data]
            # self.vendas = [Venda(venda['id'], venda['cliente_id'], venda['vendedor_id'], venda['data_venda'], venda['forma_pagamento'], venda['quantidade_parcelas']) for venda in vendas_data]
            return self.vendas
        else:
            print(f"Erro ao listar vendas: {response.json()}")
            return []

    def buscar_venda_por_id(self, id):
        response = requests.get(f"{self.api_url}/{id}")
        if response.status_code == 200:
            venda_data = response.json()
            venda = Venda(venda_data['id'], venda_data['cliente_id'], venda_data['vendedor_id'], venda_data['data_venda'], venda_data['forma_pagamento'], venda_data['quantidade_parcelas'])
            venda.itens = venda_data['itens']
            return venda
        else:
            print(f"Erro ao buscar venda por ID: {response.json()}")
            return None

    def buscar_venda_por_data(self, data_venda):
        response = requests.get(self.api_url, params={"data_venda": data_venda})
        if response.status_code == 200:
            vendas_data = response.json()
            return [Venda(venda['id'], venda['cliente_id'], venda['vendedor_id'], venda['data_venda'], venda['forma_pagamento'], venda['quantidade_parcelas']) for venda in vendas_data]
        else:
            print(f"Erro ao buscar venda por data: {response.json()}")
            return []

    def atualizar_venda(self, id, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas):
        data = {
            "cliente_id": cliente_id,
            "vendedor_id": vendedor_id,
            "data_venda": data_venda,
            "forma_pagamento": forma_pagamento,
            "quantidade_parcelas": quantidade_parcelas
        }
        response = requests.put(f"{self.api_url}/{id}", json=data)
        if response.status_code == 200:
            venda = self.buscar_venda_por_id(id)
            if venda:
                venda.cliente_id = cliente_id
                venda.vendedor_id = vendedor_id
                venda.data_venda = data_venda
                venda.forma_pagamento = forma_pagamento
                venda.quantidade_parcelas = quantidade_parcelas
        else:
            print(f"Erro ao atualizar venda: {response.json()}")

    def excluir_venda(self, id):
        response = requests.delete(f"{self.api_url}/{id}")
        if response.status_code == 200:
            self.vendas = [venda for venda in self.vendas if venda.id != id]
        else:
            print(f"Erro ao excluir venda: {response.json()}")

    def exportar_relatorio_csv(self, caminho_arquivo, dados):
        import csv
        with open(caminho_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Id", "Cliente", "Produto", "Quantidade", "Vendedor", "Forma de Pagamento", "Data"])
            for linha in dados:
                writer.writerow([linha[0], linha[1], linha[2], linha[3], linha[4], linha[5]])