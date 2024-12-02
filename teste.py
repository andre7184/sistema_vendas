import tkinter as tk
from tkinter import messagebox
import mysql.connector
import csv

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="sistema_vendas"
)
cursor = conn.cursor()

# Funções do Sistema
def cadastrar_produto():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    quantidade = entry_quantidade.get()
    valor = entry_valor.get()

    if nome and descricao and quantidade and valor:
        cursor.execute("INSERT INTO produtos (nome, descricao, quantidade, valor) VALUES (%s, %s, %s, %s)",
                       (nome, descricao, quantidade, valor))
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

def cadastrar_vendedor():
    nome = entry_nome_vendedor.get()
    login = entry_login.get()
    senha = entry_senha.get()

    if nome and login and senha:
        cursor.execute("INSERT INTO vendedores (nome, login, senha) VALUES (%s, %s, %s)",
                       (nome, login, senha))
        conn.commit()
        messagebox.showinfo("Sucesso", "Vendedor cadastrado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

def realizar_venda():
    cliente = entry_cliente.get()
    cpf = entry_cpf.get()
    endereco = entry_endereco.get()
    pagamento = entry_pagamento.get()
    produto = entry_produto.get()
    quantidade = entry_quantidade_venda.get()
    vendedor = entry_vendedor.get()

    if cliente and cpf and endereco and pagamento and produto and quantidade and vendedor:
        cursor.execute("INSERT INTO vendas (cliente, cpf, endereco, pagamento, produto, quantidade, vendedor) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (cliente, cpf, endereco, pagamento, produto, quantidade, vendedor))
        conn.commit()
        messagebox.showinfo("Sucesso", "Venda realizada com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

def gerar_relatorio():
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()

    with open('relatorio_vendas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Cliente", "CPF", "Endereço", "Pagamento", "Produto", "Quantidade", "Vendedor", "Data"])
        for venda in vendas:
            writer.writerow(venda)

    messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

# Interface gráfica
root = tk.Tk()
root.title("Sistema de Vendas")

# Cadastro de Produtos
tk.Label(root, text="Nome do Produto").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Descrição").grid(row=1, column=0)
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=1, column=1)

tk.Label(root, text="Quantidade").grid(row=2, column=0)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=2, column=1)

tk.Label(root, text="Valor Unitário").grid(row=3, column=0)
entry_valor = tk.Entry(root)
entry_valor.grid(row=3, column=1)

tk.Button(root, text="Cadastrar Produto", command=cadastrar_produto).grid(row=4, column=1)

# Cadastro de Vendedores
tk.Label(root, text="Nome do Vendedor").grid(row=5, column=0)
entry_nome_vendedor = tk.Entry(root)
entry_nome_vendedor.grid(row=5, column=1)

tk.Label(root, text="Login").grid(row=6, column=0)
entry_login = tk.Entry(root)
entry_login.grid(row=6, column=1)

tk.Label(root, text="Senha").grid(row=7, column=0)
entry_senha = tk.Entry(root, show="*")
entry_senha.grid(row=7, column=1)

tk.Button(root, text="Cadastrar Vendedor", command=cadastrar_vendedor).grid(row=8, column=1)

# Realização de Vendas
tk.Label(root, text="Cliente").grid(row=9, column=0)
entry_cliente = tk.Entry(root)
entry_cliente.grid(row=9, column=1)

tk.Label(root, text="CPF").grid(row=10, column=0)
entry_cpf = tk.Entry(root)
entry_cpf.grid(row=10, column=1)

tk.Label(root, text="Endereço").grid(row=11, column=0)
entry_endereco = tk.Entry(root)
entry_endereco.grid(row=11, column=1)

tk.Label(root, text="Forma de Pagamento").grid(row=12, column=0)
entry_pagamento = tk.Entry(root)
entry_pagamento.grid(row=12, column=1)

tk.Label(root, text="Produto").grid(row=13, column=0)
entry_produto = tk.Entry(root)
entry_produto.grid(row=13, column=1)

tk.Label(root, text="Quantidade").grid(row=14, column=0)
entry_quantidade_venda = tk.Entry(root)
entry_quantidade_venda.grid(row=14, column=1)

tk.Label(root, text="Vendedor").grid(row=15, column=0)
entry_vendedor = tk.Entry(root)
entry_vendedor.grid(row=15, column=1)

tk.Button(root, text="Realizar Venda", command=realizar_venda).grid(row=16, column=1)

# Geração de Relatório
tk.Button(root, text="Gerar Relatório", command=gerar_relatorio).grid(row=17, column=1)

root.mainloop()