from db.gerenciador_bd import GerenciadorBancoDados

class CRUD:
    def __init__(self):
        self.db_manager = GerenciadorBancoDados()

    def criar(self, tabela, colunas, valores):
        query = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(['%s'] * len(valores))})"
        return self.db_manager.executar_query(query, valores)

    def listar(self, tabela, colunas):
        query = f"SELECT {', '.join(colunas)} FROM {tabela}"
        resultados = self.db_manager.buscar_todos(query)
        return resultados

    def buscar_por_id(self, tabela, colunas, id_coluna, id_valor):
        query = f"SELECT {', '.join(colunas)} FROM {tabela} WHERE {id_coluna} = %s"
        resultado = self.db_manager.buscar_um(query, (id_valor,))
        return resultado

    def atualizar(self, tabela, colunas, valores, id_coluna, id_valor):
        set_clause = ', '.join([f"{coluna} = %s" for coluna in colunas])
        query = f"UPDATE {tabela} SET {set_clause} WHERE {id_coluna} = %s"
        self.db_manager.executar_query(query, valores + [id_valor])

    def excluir(self, tabela, id_coluna, id_valor):
        query = f"DELETE FROM {tabela} WHERE {id_coluna} = %s"
        self.db_manager.executar_query(query, (id_valor,))

    def buscar_por_condicao(self, tabela, colunas, condicao, valores):
        query = f"SELECT {', '.join(colunas)} FROM {tabela} WHERE {condicao}"
        resultado = self.db_manager.buscar_um(query, valores)
        return resultado

    def buscar_por_nome(self, tabela, colunas, nome_coluna, nome_valor):
        query = f"SELECT {', '.join(colunas)} FROM {tabela} WHERE {nome_coluna} LIKE %s"
        resultados = self.db_manager.buscar_todos(query, (f"%{nome_valor}%",))
        return resultados

    def buscar_por_data(self, tabela, colunas, data_coluna, data_valor):
        query = f"SELECT {', '.join(colunas)} FROM {tabela} WHERE {data_coluna} = %s"
        resultados = self.db_manager.buscar_todos(query, (data_valor,))
        return resultados