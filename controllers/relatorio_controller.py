from db.models import Relatorio
# from db.crud import CRUD

class RelatorioController:
    def __init__(self):
        # self.crud = CRUD()
        self.tabela = "relatorios"
        self.colunas = ["id", "cliente", "produto", "quantidade", "vendedor", "forma_pagamento", "data_venda"]

    def gerar_relatorio(self):
        # Método para gerar relatórios fictícios para teste
        return self.relatorios

    def listar_relatorio(self):
        # Descomente as linhas abaixo para usar o banco de dados
        # relatorios = self.crud.listar(self.tabela, self.colunas)
        # return [Relatorio(cliente, produto, quantidade, vendedor, forma_pagamento, data_venda) for cliente, produto, quantidade, vendedor, forma_pagamento, data_venda in relatorios]
        return self.gerar_relatorio()

    def buscar_relatorio_pela_data(self, dataIn, dataOut):
        # Descomente as linhas abaixo para usar o banco de dados
        # condicao = "data_venda BETWEEN %s AND %s"
        # valores = (dataIn, dataOut)
        # relatorios = self.crud.buscar_por_condicao(self.tabela, self.colunas, condicao, valores)
        # return [Relatorio(cliente, produto, quantidade, vendedor, forma_pagamento, data_venda) for cliente, produto, quantidade, vendedor, forma_pagamento, data_venda in relatorios]
        relatorio = self.gerar_relatorio()
        return [linha for linha in relatorio if dataIn <= linha.data_venda <= dataOut]

    def exportar_relatorio_csv(self, caminho_arquivo):
        import csv
        relatorio = self.gerar_relatorio()
        with open(caminho_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Cliente", "Produto", "Quantidade", "Vendedor", "Forma de Pagamento", "Data"])
            for linha in relatorio:
                writer.writerow([linha.cliente, linha.produto, linha.valor, linha.vendedor, linha.data_venda])