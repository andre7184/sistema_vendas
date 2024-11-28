
from db.connection import get_connection

class GerenciadorBancoDados:
    def __init__(self):
        pass

    def executar_query(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()

    def buscar_todos(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def buscar_um(self, query, params=()):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado