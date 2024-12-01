from db.models import Venda
#from db.crud import CRUD

class VendaController:
    def __init__(self):
        # self.crud = CRUD()
        self.tabela_vendas = "vendas"
        self.tabela_itens_venda = "itens_venda"
        self.colunas_vendas = ["id", "cliente_id", "vendedor_id", "data_venda", "forma_pagamento", "quantidade_parcelas"]
        self.colunas_itens_venda = ["venda_id", "produto_id", "quantidade", "valor_unitario"]
        self.vendas = []
        self.next_id = 1  # Inicializa o próximo ID

    def cadastrar_venda(self, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas=None):
        venda = Venda(self.next_id, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas)
        self.vendas.append(venda)
        self.next_id += 1

        # Persistir a venda no banco de dados
        # valores_venda = (venda.id, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas)
        # self.crud.criar(self.tabela_vendas, self.colunas_vendas, valores_venda)

        return venda

    def adicionar_item_venda(self, venda_id, produto_id, quantidade, valor_unitario):
        venda = next((v for v in self.vendas if v.id == venda_id), None)
        if venda:
            venda.adicionar_item(produto_id, quantidade, valor_unitario)

            # Persistir o item da venda no banco de dados
            # valores_item_venda = (venda_id, produto_id, quantidade, valor_unitario)
            # self.crud.criar(self.tabela_itens_venda, self.colunas_itens_venda, valores_item_venda)

    def calcular_total(self, produtos_adicionados):
        total_valor = 0
        for produto in produtos_adicionados:
            quantidade = int(produto[2])
            valor_unitario = float(produto[3])
            desconto = float(produto[4]) / 100  # Converte a porcentagem de desconto para um valor decimal
            valor_com_desconto = valor_unitario * (1 - desconto)
            total_valor += valor_com_desconto * quantidade
        return total_valor

    def buscar_dados_cliente(self, cliente_controller, nome_cliente):
        return cliente_controller.buscar_cliente_por_nome(nome_cliente)

    def buscar_dados_produto(self, produto_controller, nome_produto):
        return produto_controller.buscar_produto_por_nome(nome_produto)

    def registrar_venda(self, venda):
        cliente_id = venda["cliente"]["id"]
        vendedor_id = venda["vendedor"]["id"]  # pega o id do vendedor logado no sistema no main app
        data_venda = venda["data"]  # Data atual
        forma_pagamento = venda["forma_pagamento"]
        quantidade_parcelas = venda["parcelas"]

        nova_venda = self.cadastrar_venda(cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas)

        for item in venda["produtos"]:
            produto_id = item[0]
            quantidade = item[2]
            valor_unitario = item[3]
            self.adicionar_item_venda(nova_venda.id, produto_id, quantidade, valor_unitario)

        # Persistir a venda no banco de dados
        # valores_venda = (nova_venda.id, cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas)
        # self.crud.criar(self.tabela_vendas, self.colunas_vendas, valores_venda)

        return nova_venda

    def adicionar_produto(self, produtos_adicionados, produto_id, produto_nome, quantidade, valor_unitario):
        valor_total = quantidade * float(valor_unitario)
        produtos_adicionados.append((produto_id, produto_nome, quantidade, valor_unitario, 0, valor_total))
        return produtos_adicionados

    def atualizar_totais(self, produtos_adicionados):
        total_quantidade = sum(int(produto[2]) for produto in produtos_adicionados)
        total_valor = self.calcular_total(produtos_adicionados)
        return len(produtos_adicionados), total_quantidade, total_valor

    def excluir_produto(self, produtos_adicionados, produto_id):
        produtos_adicionados = [p for p in produtos_adicionados if p[0] != produto_id]
        return produtos_adicionados

    def editarPrProduto(self, produtos_adicionados, produto_id, nova_porcentagem):
        for i, produto in enumerate(produtos_adicionados):
            if produto[0] == produto_id:
                valor_total = float(produto[3]) * float(produto[2]) * (1 - float(nova_porcentagem) / 100)
                produtos_adicionados[i] = (produto[0], produto[1], produto[2], produto[3], nova_porcentagem, valor_total)
                break
        return produtos_adicionados

    def editarQtdProduto(self, produtos_adicionados, produto_id, nova_quantidade):
        for i, produto in enumerate(produtos_adicionados):
            if produto[0] == produto_id:
                valor_total = float(produto[3]) * float(nova_quantidade) * (1 - float(produto[4]) / 100)
                produtos_adicionados[i] = (produto[0], produto[1], nova_quantidade, produto[3], produto[4], valor_total)
                break
        return produtos_adicionados