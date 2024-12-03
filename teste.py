import tkinter as tk
from tkinter import messagebox
import mysql.connector
import csv

class SistemaVendas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas")
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)

        # Conexão com o banco de dados
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sistema_vendas_teste"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
            self.root.destroy()
        
        self.tela_login()

    def tela_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.entry_login = tk.Entry(self.root)
        self.entry_login.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Senha").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=1, pady=10)

    def login(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()

        self.cursor.execute("SELECT id, nome, tipo FROM usuarios WHERE login = %s AND senha = %s", (login, senha))
        usuario = self.cursor.fetchone()

        if usuario:
            self.usuario_logado = usuario
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario[1]}!")
            self.abrir_menu(usuario[2])
        else:
            messagebox.showerror("Erro", "Login ou senha incorretos!")

    def abrir_menu(self, tipo_usuario):
        for widget in self.root.winfo_children():
            widget.destroy()

        if tipo_usuario == 'Administrador':
            tk.Button(self.root, text="Cadastrar Produto", command=self.abrir_cadastro_produto).grid(row=0, column=0, pady=10)
            tk.Button(self.root, text="Cadastrar Usuário", command=self.abrir_cadastro_usuario).grid(row=1, column=0, pady=10)
            tk.Button(self.root, text="Gerar Relatório", command=self.gerar_relatorio).grid(row=2, column=0, pady=10)
        elif tipo_usuario == 'Vendedor':
            tk.Button(self.root, text="Realizar Venda", command=self.abrir_realizar_venda).grid(row=0, column=0, pady=10)
            tk.Button(self.root, text="Visualizar Relatório", command=self.gerar_relatorio).grid(row=1, column=0, pady=10)

        tk.Button(self.root, text="Logout", command=self.logout).grid(row=3, column=0, pady=10)

    def abrir_cadastro_produto(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Nome do Produto").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Descrição").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_descricao = tk.Entry(self.root)
        self.entry_descricao.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Quantidade").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.entry_quantidade = tk.Entry(self.root)
        self.entry_quantidade.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Valor Unitário").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.entry_valor = tk.Entry(self.root)
        self.entry_valor.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Cadastrar Produto", command=self.cadastrar_produto).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Voltar Menu", command=lambda: self.abrir_menu(self.usuario_logado[2])).grid(row=4, column=2, pady=10)

    def abrir_cadastro_usuario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Nome do Usuário").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.entry_nome_usuario = tk.Entry(self.root)
        self.entry_nome_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Login").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_login = tk.Entry(self.root)
        self.entry_login.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Senha").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Tipo (Administrador/Vendedor)").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.entry_tipo = tk.Entry(self.root)
        self.entry_tipo.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Cadastrar Usuário", command=self.cadastrar_usuario).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Voltar Menu", command=lambda: self.abrir_menu(self.usuario_logado[2])).grid(row=4, column=2, pady=10)

    def abrir_realizar_venda(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Cliente").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.entry_cliente = tk.Entry(self.root)
        self.entry_cliente.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="CPF").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_cpf = tk.Entry(self.root)
        self.entry_cpf.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Endereço").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.entry_endereco = tk.Entry(self.root)
        self.entry_endereco.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Forma de Pagamento").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.forma_pagamento_var = tk.StringVar(self.root)
        self.forma_pagamento_var.set("À vista")  # Valor padrão
        self.option_menu_pagamento = tk.OptionMenu(self.root, self.forma_pagamento_var, "À vista", "Parcelado", command=self.atualizar_parcelas)
        self.option_menu_pagamento.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Parcelas").grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self.entry_parcelas = tk.Entry(self.root)
        self.entry_parcelas.grid(row=4, column=1, padx=10, pady=10)
        self.entry_parcelas.insert(0, "1")  # Valor padrão para "À vista"
        self.entry_parcelas.config(state='readonly')  # Inicialmente em modo somente leitura

        # Vendedor é o usuário atual logado
        tk.Label(self.root, text="Vendedor").grid(row=5, column=0, sticky="e", padx=10, pady=10)
        self.entry_vendedor = tk.Entry(self.root)
        self.entry_vendedor.insert(0, self.usuario_logado[0])  # Insere o ID do usuário logado
        self.entry_vendedor.config(state='readonly')
        self.entry_vendedor.grid(row=5, column=1, padx=10, pady=10)

        # Botão para abrir a janela de seleção de produtos
        tk.Button(self.root, text="Adicionar Produto", command=self.abrir_selecao_produtos).grid(row=6, column=1, pady=10)

        # Lista de produtos selecionados
        self.lista_produtos_vendidos = []
        self.label_produtos_selecionados = tk.Frame(self.root)
        self.label_produtos_selecionados.grid(row=7, column=0, columnspan=2)

        tk.Button(self.root, text="Realizar Venda", command=self.realizar_venda).grid(row=8, column=1, pady=10)
        tk.Button(self.root, text="Voltar Menu", command=lambda: self.abrir_menu(self.usuario_logado[2])).grid(row=8, column=2, pady=10)
    
    def atualizar_parcelas(self, value):
        if value == "À vista":
            self.entry_parcelas.config(state='normal')
            self.entry_parcelas.delete(0, tk.END)
            self.entry_parcelas.insert(0, "1")
            self.entry_parcelas.config(state='readonly')
        else:
            self.entry_parcelas.config(state='normal')
            self.entry_parcelas.delete(0, tk.END)

    def adicionar_produto_vendido(self):
        produto_id = self.entry_produto_id.get()
        quantidade = self.entry_quantidade_venda.get()
        valor_unitario = self.entry_valor_unitario.get()

        if produto_id and quantidade and valor_unitario:
            self.lista_produtos_vendidos.append({
                'produto_id': produto_id,
                'quantidade': quantidade,
                'valor_unitario': valor_unitario
            })
            messagebox.showinfo("Sucesso", "Produto adicionado à venda!")
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

    def atualizar_lista_produtos(self):
        texto = "\n".join([f"{produto[1]} - R${produto[2]:.2f}" for produto in self.lista_produtos_vendidos])
        self.label_produtos_selecionados.config(text=texto)   

    def adicionar_produtos_selecionados(self):
        selecionados = self.lista_produtos.curselection()
        total_labels = []
        quantidade_entries = []

        for i in selecionados:
            produto_info = self.lista_produtos.get(i)
            produto_id = produto_info.split(" - ")[0]
            self.cursor.execute("SELECT id, nome, valor FROM produtos WHERE nome = %s", (produto_id,))
            produto = self.cursor.fetchone()
            produto_dict = {
                'produto_id': produto[0],
                'nome': produto[1],
                'quantidade': 1,
                'valor_unitario': produto[2]
            }
            self.lista_produtos_vendidos.append(produto_dict)
            row = len(self.lista_produtos_vendidos) - 1
            tk.Label(self.label_produtos_selecionados, text=f"{produto[1]} - R${produto[2]:.2f}").grid(row=row, column=0)
            
            quantidade_entry = tk.Entry(self.label_produtos_selecionados)
            quantidade_entry.insert(0, "1")
            quantidade_entry.grid(row=row, column=1)
            quantidade_entry.bind("<KeyRelease>", lambda event, idx=row: self.calcular_total(event, idx))
            quantidade_entries.append(quantidade_entry)
            
            total_label = tk.Label(self.label_produtos_selecionados, text=f"R${produto[2]:.2f}")
            total_label.grid(row=row, column=2)
            total_labels.append(total_label)

        self.quantidade_entries = quantidade_entries
        self.total_labels = total_labels

    def calcular_total(self, event, i):
        quantidade = int(self.quantidade_entries[i].get())
        valor_unitario = float(self.lista_produtos_vendidos[i]['valor_unitario'])
        total = quantidade * valor_unitario
        self.total_labels[i].config(text=f"R${total:.2f}")

    def abrir_selecao_produtos(self):
        self.janela_produtos = tk.Toplevel(self.root)
        self.janela_produtos.title("Seleção de Produtos")
        
        self.lista_produtos = tk.Listbox(self.janela_produtos, selectmode=tk.MULTIPLE)
        self.lista_produtos.pack(padx=10, pady=10)
        
        self.cursor.execute("SELECT id, nome, valor FROM produtos")
        produtos = self.cursor.fetchall()
        
        for produto in produtos:
            self.lista_produtos.insert(tk.END, f"{produto[1]} - R${produto[2]:.2f}")
        
        tk.Button(self.janela_produtos, text="Adicionar", command=self.adicionar_produtos_selecionados).pack(pady=10)

    def cadastrar_produto(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        quantidade = self.entry_quantidade.get()
        valor = self.entry_valor.get()

        if nome and descricao and quantidade and valor:
            self.cursor.execute("INSERT INTO produtos (nome, descricao, quantidade, valor) VALUES (%s, %s, %s, %s)",
                                (nome, descricao, quantidade, valor))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.abrir_menu(self.usuario_logado[2])
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

    def cadastrar_usuario(self):
        nome = self.entry_nome_usuario.get()
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        tipo = self.entry_tipo.get()

        if nome and login and senha and tipo:
            self.cursor.execute("INSERT INTO usuarios (nome, login, senha, tipo) VALUES (%s, %s, %s, %s)",
                                (nome, login, senha, tipo))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.abrir_menu(self.usuario_logado[2])
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

    def realizar_venda(self):
        cliente = self.entry_cliente.get()
        cpf = self.entry_cpf.get()
        endereco = self.entry_endereco.get()
        pagamento = self.forma_pagamento_var.get()
        qtd_parcelas = int(self.entry_parcelas.get())
        vendedor = int(self.entry_vendedor.get())

        if cliente and cpf and endereco and pagamento and qtd_parcelas and vendedor:
            # Atualiza as quantidades na lista de produtos vendidos
            for i in range(len(self.lista_produtos_vendidos)):
                quantidade_entry = self.label_produtos_selecionados.grid_slaves(row=i, column=1)[0]
                quantidade = int(quantidade_entry.get())
                valor_unitario = float(self.lista_produtos_vendidos[i]['valor_unitario'])
                total_label = self.label_produtos_selecionados.grid_slaves(row=i, column=2)[0]
                total_label.config(text=f"R${quantidade * valor_unitario:.2f}")
                self.lista_produtos_vendidos[i]['quantidade'] = quantidade

            # Insere a venda no banco de dados
            self.cursor.execute(
                "INSERT INTO vendas (cliente_nome, cliente_cpf, cliente_endereco, forma_pagamento, qtd_parcelas, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (cliente, cpf, endereco, pagamento, qtd_parcelas, vendedor)
            )
            venda_id = self.cursor.lastrowid

            # Insere os itens da venda no banco de dados
            produtos_vendidos = []
            for item in self.lista_produtos_vendidos:
                produto_id = item['produto_id']
                quantidade = item['quantidade']
                valor_unitario = item['valor_unitario']
                produtos_vendidos.append((venda_id, produto_id, quantidade, valor_unitario))

            self.cursor.executemany(
                "INSERT INTO itens_vendas (venda_id, produto_id, quantidade, valor_unitario) VALUES (%s, %s, %s, %s)",
                produtos_vendidos
            )

            # Confirma a transação
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Venda realizada com sucesso!")
            self.abrir_menu(self.usuario_logado[2])
        else:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios!")

    def gerar_relatorio(self):
        self.cursor.execute("SELECT * FROM vendas")
        vendas = self.cursor.fetchall()

        with open('relatorio_vendas.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Cliente", "CPF", "Endereço", "Pagamento", "Produto", "Quantidade", "Vendedor", "Data"])
            for venda in vendas:
                self.cursor.execute("SELECT * FROM itens_vendas WHERE venda_id = %s", (venda[0],))
                itens = self.cursor.fetchall()
                for item in itens:
                    writer.writerow([venda[1], venda[2], venda[3], venda[4], item[2], item[3], venda[5], venda[6]])

        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

    def logout(self):
        self.usuario_logado = None
        self.tela_login()

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVendas(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar_conexao)
    root.mainloop()