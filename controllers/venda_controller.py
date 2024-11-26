from db.models import Venda
# from db.connection import get_connection

class VendaController:
    def __init__(self):
        self.vendas = []

    def cadastrar_venda(self, cliente, produto, quantidade, vendedor, forma_pagamento):
        venda = Venda(cliente, vendedor, "2024-11-26", forma_pagamento)
        venda.adicionar_item(produto, quantidade, produto.valor)
        self.vendas.append(venda)
        # Descomente as linhas abaixo para usar o banco de dados
        # conn = get_connection()
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO vendas (cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas) VALUES (%s, %s, %s, %s, %s)",
        #                (venda.cliente.id, venda.vendedor.id, venda.data_venda, venda.forma_pagamento, venda.quantidade_parcelas))
        # venda_id = cursor.lastrowid
        # for item in venda.itens:
        #     cursor.execute("INSERT INTO itens_venda (venda_id, produto_id, quantidade, valor_unitario) VALUES (%s, %s, %s, %s)",
        #                    (venda_id, item['produto'].id, item['quantidade'], item['valor_unitario']))
        # conn.commit()
        # cursor.close()
        # conn.close()
        return venda

    def listar_vendas(self):
        # Descomente as linhas abaixo para usar o banco de dados
        # conn = get_connection()
        # cursor = conn.cursor()
        # cursor.execute("SELECT cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas FROM vendas")
        # vendas = cursor.fetchall()
        # cursor.close()
        # conn.close()
        # return [Venda(cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas) for cliente_id, vendedor_id, data_venda, forma_pagamento, quantidade_parcelas in vendas]
        return self.vendas