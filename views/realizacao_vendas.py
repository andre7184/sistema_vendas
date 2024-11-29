import tkinter as tk
from tkinter import ttk
from components.grid import Grid
from views.cadastro_cliente import CadastroCliente

class RealizacaoVendas(tk.Frame):
    def __init__(self, master, venda_controller, produto_controller, cliente_controller):
        super().__init__(master)
        self.venda_controller = venda_controller
        self.produto_controller = produto_controller
        self.cliente_controller = cliente_controller
        self.produtos_selecionados = []
        self.cliente_selecionado = None
        self.create_widgets()

    def create_widgets(self):
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.frame_venda = tk.Frame(self)
        self.frame_venda.pack(pady=10, fill=tk.X, expand=True, anchor='n')

        self.label_titulo = tk.Label(self.frame_venda, text="Realizar Venda", font=("Arial", 16))
        self.label_titulo.pack(pady=10)

        # Seção de Cliente
        self.frame_cliente = tk.Frame(self.frame_venda)
        self.frame_cliente.pack(pady=5, fill=tk.X)

        self.label_buscar_cliente, self.entry_buscar_cliente = self.addFrameBuscar(self.frame_cliente, "Cliente", tk.NORMAL, self.buscar_cliente)


        # Frame para Treeview com Scrollbar do CLIENTE
        self.frame_treeview_cliente, self.treeview_cliente = self.create_table(self.frame_venda, columns=("ID", "Nome", "CPF", "Endereço"), height=3)
        self.frame_treeview_cliente.pack(pady=5, fill=tk.BOTH, expand=True)

        # Frame para exibir os dados do cliente selecionado
        self.frame_dados_cliente = tk.Frame(self.frame_venda)
        
        # Label para exibir os dados do cliente selecionado
        self.label_dados_cliente = tk.Label(self.frame_dados_cliente, text="", font=("Arial", 12))
        self.label_dados_cliente.pack(side=tk.LEFT, padx=5)
        
        # Botão para editar o cliente selecionado
        self.btn_editar_cliente = tk.Button(self.frame_dados_cliente, text="Editar Cliente", command=self.editar_cliente)
        self.btn_editar_cliente.pack(side=tk.LEFT, padx=5)

        # Adiciona o frame dos dados do cliente logo após o campo de busca
        self.frame_dados_cliente.pack(pady=5, fill=tk.X, expand=True)

        # Seção de Produtos
        self.frame_produtos = tk.Frame(self.frame_venda)
        self.frame_produtos.pack(pady=5, fill=tk.X)
        
        self.label_buscar_produto, self.entry_buscar_produto = self.addFrameBuscar(self.frame_produtos, "Produto", tk.DISABLED, self.buscar_produto)

        # Frame para Treeview com Scrollbar do PRODUTO
        self.frame_treeview_produtos, self.treeview_produtos = self.create_table(self.frame_venda, columns=("ID", "Nome", "Quantidade", "Valor"), height=3)
        self.frame_treeview_produtos.pack(pady=5, fill=tk.X, expand=True)

        # Campo de quantidade e botão adicionar produto
        self.frame_adicionar_produto = tk.Frame(self.frame_venda)
        self.frame_adicionar_produto.pack(pady=5)

        # inicia a quantidade como 1
        self.entry_quantidade = tk.Entry(self.frame_adicionar_produto, width=5, state=tk.NORMAL)
        self.entry_quantidade.insert(0, 1)
        self.entry_quantidade.pack(side=tk.LEFT, padx=5)
        self.entry_quantidade.config(state=tk.DISABLED)

        self.btn_adicionar_produto = tk.Button(self.frame_adicionar_produto, text="Adicionar Produto", command=self.adicionar_produto, state=tk.DISABLED)
        self.btn_adicionar_produto.pack(side=tk.LEFT, padx=5)

        # Frame para exibir os produto selecionados com altura fixa e com scrollbar
        self.frame_gred_view = tk.Frame(self.frame_venda)
        self.frame_gred_view.pack(pady=5, fill=tk.X, expand=True)

        # Mostrar quantidade de produtos e valor total ao final da tabela
        self.total_frame = tk.Frame(self.frame_venda)
        self.total_frame.pack(pady=10)

        self.label_total_quantidade = tk.Label(self.total_frame, text="Total de Produtos: 0")
        self.label_total_quantidade.pack(side=tk.LEFT, padx=5)

        self.label_total_valor = tk.Label(self.total_frame, text="Valor Total: 0.00")
        self.label_total_valor.pack(side=tk.LEFT, padx=5)
    
    def addFrameBuscar(self, frame, texto, state, callback):
        label = tk.Label(frame, text=texto, font=("Arial", 14))
        label.pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, state=state, width=50)  
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind("<KeyRelease>", callback)
        return label, entry 

    def create_table(self, frame, columns, height, editable_columns=(), bind_double_click=None):
        frame_treeview = tk.Frame(frame)
        treeview = ttk.Treeview(frame_treeview, columns=columns, show="headings", height=height)
        
        for col in columns:
            treeview.heading(col, text=col)
            if col in editable_columns:
                treeview.column(col, width=100, anchor='center')
        
        scrollbar = tk.Scrollbar(frame_treeview, command=treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        treeview.config(yscrollcommand=scrollbar.set)
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        if bind_double_click:
            treeview.bind('<Double-1>', bind_double_click)
        
        return frame_treeview, treeview

    def buscar_cliente(self, event=None):
        nome_cliente = self.entry_buscar_cliente.get()
        clientes = self.cliente_controller.buscar_cliente_por_nome(nome_cliente)
        if clientes:
            # Exibir a tabela de clientes logo após o campo de busca
            self.frame_treeview_cliente.pack_forget()  # Esconde a tabela antes de reempacotar
            self.frame_treeview_cliente.pack(pady=5, fill=tk.BOTH, expand=True, after=self.frame_cliente)
            
            # Limpar a tabela antes de inserir novos dados
            for item in self.treeview_cliente.get_children():
                self.treeview_cliente.delete(item)

            for cliente in clientes:
                self.treeview_cliente.insert("", "end",
                                            values=(cliente.id,
                                                    cliente.nome,
                                                    cliente.cpf,
                                                    cliente.endereco))
            # Vincular evento de clique na tabela de clientes
            if not hasattr(self.treeview_cliente, 'bound'):
                self.treeview_cliente.bind("<ButtonRelease-1>", self.on_treeview_click)
                setattr(self.treeview_cliente, 'bound', True)
            
            # Limpar o texto da label_dados_cliente e desativar o botão btn_editar_cliente
            self.label_dados_cliente.config(text="")
            self.btn_editar_cliente.config(state=tk.DISABLED)
            self.entry_buscar_produto.config(state=tk.DISABLED)
            self.entry_quantidade.config(state=tk.DISABLED)
            self.btn_adicionar_produto.config(state=tk.DISABLED)

    def on_treeview_click(self, event):
        item = self.treeview_cliente.identify('item', event.x, event.y)
        cliente_id = int(self.treeview_cliente.item(item, "values")[0])
        cliente_nome = str(self.treeview_cliente.item(item,"values")[1])
        cliente_cpf = str(self.treeview_cliente.item(item,"values")[2])
        cliente_endereco = str(self.treeview_cliente.item(item,"values")[3])
        
        # Selecionar o cliente e exibir os dados na label
        if cliente_id:
            cliente_info = f"ID: {cliente_id}, Nome: {cliente_nome}, CPF: {cliente_cpf}, Endereço: {cliente_endereco}"
            self.label_dados_cliente.config(text=cliente_info)
            self.frame_dados_cliente.pack(pady=5, fill=tk.BOTH, expand=True)
            
            # Esconder a tabela de clientes
            self.frame_treeview_cliente.pack_forget()
            
            # Ativar os campos e botões de produtos
            self.btn_editar_cliente.config(state=tk.NORMAL)
            self.entry_buscar_produto.config(state=tk.NORMAL)
            self.entry_quantidade.config(state=tk.NORMAL)
            self.btn_adicionar_produto.config(state=tk.NORMAL)

    def editar_cliente(self):
        if self.cliente_selecionado:
            self.clear_frame()
            self.cadastro_cliente_frame = CadastroCliente(self, self.cliente_controller, self.cliente_selecionado)
            self.cadastro_cliente_frame.pack()

    def buscar_produto(self, event=None):
        nome_produto = self.entry_buscar_produto.get()
        produtos = self.produto_controller.buscar_produto_por_nome(nome_produto)
        self.treeview_produtos.delete(*self.treeview_produtos.get_children())
        for produto in produtos:
            self.treeview_produtos.insert("", "end", values=(produto.id, produto.nome, produto.quantidade, produto.valor))

    def adicionar_produto(self):
        selected_items = self.treeview_produtos.selection()
        if not selected_items:
            return  # Nenhum item selecionado

        selected_item = selected_items[0]
        produto = self.treeview_produtos.item(selected_item, "values")
        quantidade = int(self.entry_quantidade.get())
        self.produtos_selecionados.append((produto[0], produto[1], quantidade, produto[3], 0))
        self.treeview_produtos.delete(selected_item)

        # Adicionar linha à grade existente ou criar nova grade
        if hasattr(self, 'grid_produtos'):
            self.grid_produtos.add_row((produto[0], produto[1], quantidade, produto[3], 0))
        else:
            self.atualizar_grid_produtos()

        self.atualizar_totais()  # Atualiza os totais após adicionar o produto

    def atualizar_grid_produtos(self):
        colunas = ["ID", "Nome", "Quantidade", "Valor Unitário", "Desconto"]
        dados = self.produtos_selecionados

        # Destruir a instância anterior de Grid, se existir
        if hasattr(self, 'grid_produtos'):
            self.grid_produtos.destroy()

        self.grid_produtos = Grid(self.frame_gred_view, colunas, dados, None, self.excluir_produto, condicao_especial=True)
        self.grid_produtos.pack(pady=5, fill=tk.BOTH, expand=True)
        self.atualizar_totais()  # Atualiza os totais após atualizar a grade

    def excluir_produto(self, produto):
        self.produtos_selecionados = [p for p in self.produtos_selecionados if p != produto]
        self.grid_produtos.remove_row(produto)
        self.atualizar_totais()  

    def atualizar_totais(self):
        total_quantidade = sum(int(produto[2]) for produto in self.produtos_selecionados)
        total_valor = sum(float(produto[3]) * int(produto[2]) for produto in self.produtos_selecionados)
        self.label_total_quantidade.config(text=f"Total de Produtos: {total_quantidade}")
        self.label_total_valor.config(text=f"Valor Total: {total_valor:.2f}")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()