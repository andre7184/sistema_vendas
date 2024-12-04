import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="andre",
        password="Amb@8484",
        database="sistema_vendas"
    )