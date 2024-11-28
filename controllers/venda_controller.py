from db.models import Venda
#from db.crud import CRUD

class VendaController:
    def __init__(self):
        #self.crud = CRUD()
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