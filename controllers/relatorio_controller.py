class RelatorioController:
    def __init__(self, venda_controller):
        self.venda_controller = venda_controller

    def gerar_relatorio(self):
        vendas = self.venda_controller.listar_vendas()
        relatorio = []
        for venda in vendas:
            for item in venda.itens:
                relatorio.append({
                    'cliente': venda.cliente.nome,
                    'produto': item['produto'].nome,
                    'quantidade': item['quantidade'],
                    'vendedor': venda.vendedor.nome,
                    'forma_pagamento': venda.forma_pagamento,
                    'data_venda': venda.data_venda
                })
        return relatorio

    def exportar_relatorio_csv(self, caminho_arquivo):
        import csv
        relatorio = self.gerar_relatorio()
        with open(caminho_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Cliente", "Produto", "Quantidade", "Vendedor", "Forma de Pagamento", "Data"])
            for linha in relatorio:
                writer.writerow([linha['cliente'], linha['produto'], linha['quantidade'], linha['vendedor'], linha['forma_pagamento'], linha['data_venda']])