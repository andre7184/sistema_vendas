import tkinter as tk
from tkinter import messagebox
from components.grid import Grid
from views.cadastro_cliente import CadastroCliente
import locale

# Configura o locale para o formato de moeda brasileira
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
class RealizacaoVendas(tk.Frame):
    def __init__(self, master, venda_controller, produto_controller, cliente_controller):
        super().__init__(master)
        self.venda_controller = venda_controller
        self.produto_controller = produto_controller
        self.cliente_controller = cliente_controller
        self.produtos_adicionados = []
        self.cliente_selecionado = None
        self.lista_clientes = None
        self.create_widgets()

    def create_widgets(self):
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.frame_venda = tk.Frame(self)
        self.frame_venda.pack(pady=10, fill=tk.X, expand=True, anchor='n')
        self.label_titulo = tk.Label(self.frame_venda, text="Realizar Venda", font=("Arial", 16))
        self.label_titulo.pack(pady=10)
        # Seção de Cliente
        self.frame_cliente = self.create_section(self.frame_venda, "Cliente", self.buscar_cliente)
        self.lista_clientes = self.create_lista_clientes()
        self.lista_clientes.tree.bind('<<TreeviewSelect>>', self.onSelectClientes)
        self.frame_dados_cliente = self.create_dados_cliente(self.frame_venda)
        # Seção de Produtos
        self.frame_produtos = self.create_section(self.frame_venda, "Produto", self.buscar_produto, tk.DISABLED)
        self.lista_produtos = Grid(self.frame_venda, ["ID", "Nome", "Quantidade", "Valor"], [], 3)
        self.lista_produtos.pack(pady=5, fill=tk.BOTH, expand=True)
        self.frame_adicionar_produto = self.create_adicionar_produto(self.frame_venda)
        # Frame para exibir os produtos selecionados
        self.frame_grid_view = tk.Frame(self.frame_venda)
        self.frame_grid_view.pack(pady=5, fill=tk.X, expand=True)
        # Mostrar quantidade de produtos e valor total ao final da tabela
        self.total_frame = self.create_total_frame(self.frame_venda)

    def create_lista_clientes(self):
        if self.lista_clientes:
            self.lista_clientes.pack_forget()  # Esconde a grid existente
        frame = Grid(self.frame_venda, ["ID", "Nome", "CPF", "Endereço"], [], 3)
        frame.pack(pady=5, fill=tk.BOTH, expand=True)
        return frame

    def create_section(self, parent, label_text, callback, state=tk.NORMAL):
        frame = tk.Frame(parent)
        frame.pack(pady=5, fill=tk.X)
        label, entry = self.addFrameBuscar(frame, label_text, state, callback)
        setattr(self, f"entry_buscar_{label_text.lower()}", entry)  # Armazena a referência do campo de entrada
        return frame

    def create_dados_cliente(self, parent):
        frame = tk.Frame(parent)
        self.label_dados_cliente = tk.Label(frame, text="", font=("Arial", 12))
        self.label_dados_cliente.pack(side=tk.LEFT, padx=5)
        self.btn_editar_cliente = tk.Button(frame, text="Editar Cliente", command=self.editar_cliente)
        self.btn_editar_cliente.pack(side=tk.LEFT, padx=5)
        frame.pack(pady=5, fill=tk.X, expand=True)
        return frame

    def create_adicionar_produto(self, parent):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        self.entry_quantidade = tk.Entry(frame, width=5, state=tk.NORMAL)
        self.entry_quantidade.insert(0, 1)
        self.entry_quantidade.pack(side=tk.LEFT, padx=5)
        self.entry_quantidade.config(state=tk.DISABLED)
        self.btn_adicionar_produto = tk.Button(frame, text="Adicionar Produto", command=self.adicionar_produto, state=tk.DISABLED)
        self.btn_adicionar_produto.pack(side=tk.LEFT, padx=5)
        return frame

    def create_total_frame(self, parent):
        frame = tk.Frame(parent)
        frame.pack(pady=10)
        self.label_total_itens = tk.Label(frame, text="Total de Itens: 0")
        self.label_total_itens.pack(side=tk.LEFT, padx=5)
        self.label_total_quantidade = tk.Label(frame, text="Total de Produtos: 0")
        self.label_total_quantidade.pack(side=tk.LEFT, padx=5)
        self.label_total_valor = tk.Label(frame, text="Valor Total: 0.00")
        self.label_total_valor.pack(side=tk.LEFT, padx=5)
        return frame

    def createEditProdutos(self, frame, texto, width=10, function_callback=None):
        label_editar_produto = tk.Label(frame, text=texto, font=("Arial", 14))
        label_editar_produto.pack(side=tk.LEFT, padx=5)
        entry_editar_produto = tk.Entry(frame, state=tk.DISABLED, width=width) 
        entry_editar_produto.pack(side=tk.LEFT, padx=5)
        entry_editar_produto.bind("<KeyRelease>", function_callback)
        return entry_editar_produto

    def addFrameBuscar(self, frame, texto, state, callback):
        label = tk.Label(frame, text=texto, font=("Arial", 14))
        label.pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, state=state, width=50) 
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind("<KeyRelease>", callback)
        return label, entry 

    def buscar_cliente(self, event=None):
        nome_cliente = self.entry_buscar_cliente.get()
        clientes = self.cliente_controller.buscar_cliente_por_nome(nome_cliente)
        if clientes:
            dados_clientes = [(cliente.id, cliente.nome, cliente.cpf, cliente.endereco) for cliente in clientes]
            self.lista_clientes.update_data(dados_clientes)
            # Limpar o texto da label_dados_cliente e desativar o botão btn_editar_cliente
            self.label_dados_cliente.config(text="")
            self.btn_editar_cliente.config(state=tk.DISABLED)
            self.entry_buscar_produto.config(state=tk.DISABLED)
            self.entry_quantidade.config(state=tk.DISABLED)
            self.btn_adicionar_produto.config(state=tk.DISABLED)

    def buscar_produto(self, event=None):
        nome_produto = self.entry_buscar_produto.get()
        produtos = self.produto_controller.buscar_produto_por_nome(nome_produto)
        dados_produtos = [(produto.id, produto.nome, produto.quantidade, produto.valor) for produto in produtos]
        # Atualizar a grid de produtos
        self.lista_produtos.update_data(dados_produtos)

    def onSelectClientes(self, event):
        selected_item = self.lista_clientes.tree.selection()[0]
        print(f"Item selecionado: {selected_item}")
        cliente_id = self.lista_clientes.tree.item(selected_item)['values'][0]
        cliente_nome = self.lista_clientes.tree.item(selected_item)['values'][1]
        cliente_cpf = self.lista_clientes.tree.item(selected_item)['values'][2]
        cliente_endereco = self.lista_clientes.tree.item(selected_item)['values'][3]
        cliente_info = f"ID: {cliente_id}, Nome: {cliente_nome}, CPF: {cliente_cpf}, Endereço: {cliente_endereco}"
        self.label_dados_cliente.config(text=cliente_info)
        self.btn_editar_cliente.config(state=tk.NORMAL)
        self.entry_buscar_produto.config(state=tk.NORMAL)
        self.entry_quantidade.config(state=tk.NORMAL)
        self.btn_adicionar_produto.config(state=tk.NORMAL)
        self.lista_clientes.pack_forget()

    def editar_cliente(self):
        selected_item = self.lista_clientes.tree.selection()[0]
        cliente_id = self.lista_clientes.tree.item(selected_item)['values'][0]
        cliente_obj = self.cliente_controller.buscar_cliente_por_id(cliente_id)
        self.clear_frame()
        self.cadastro_cliente_frame = CadastroCliente(self.master, self.cliente_controller, cliente_obj)
        self.cadastro_cliente_frame.pack()

    def adicionar_produto(self):
        if self.lista_produtos.tree.selection():
            selected_item = self.lista_produtos.tree.selection()[0]
            produto_id = self.lista_produtos.tree.item(selected_item)['values'][0]
            produto_nome = self.lista_produtos.tree.item(selected_item)['values'][1]
            produto_valor = self.lista_produtos.tree.item(selected_item)['values'][3]
            quantidade = int(self.entry_quantidade.get())
            self.produtos_adicionados.append((produto_id, produto_nome, quantidade, produto_valor, 0))
            self.lista_produtos.tree.delete(selected_item)
            if hasattr(self, 'grid_produtos'):
                self.grid_produtos.add_row((produto_id, produto_nome, quantidade, produto_valor, 0))
            else:
                self.atualizar_grid_produtos()
            self.atualizar_totais()
        else:
            messagebox.showerror("Erro", "Selecione um produto para adicionar.")

    def atualizar_grid_produtos(self):
        colunas = ["ID", "Nome", "Quantidade", "Valor Unitário", "Desconto"]
        dados = self.produtos_adicionados
        if hasattr(self, 'grid_produtos'):
            self.grid_produtos.destroy()

        # Frame para os botões
        self.frame_editar_produto = tk.Frame(self.frame_grid_view)
        self.frame_editar_produto.pack(pady=5, fill=tk.X)
        self.btn_excluir_produto = tk.Button(self.frame_editar_produto, text="Excluir Produto", state=tk.DISABLED, command=self.excluir_produto)
        self.btn_excluir_produto.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry_editar_qtd_produto = self.createEditProdutos(self.frame_editar_produto, "Editar Quantidade:", width=5, function_callback=self.editarQtdProduto)
        self.entry_editar_pr_produto = self.createEditProdutos(self.frame_editar_produto, "Editar Porcentagem:", width=10, function_callback=self.editarPrProduto)
        self.grid_produtos = Grid(self.frame_grid_view, colunas, dados, 4)
        self.grid_produtos.pack(pady=5, fill=tk.BOTH, expand=True)
        self.grid_produtos.tree.bind('<<TreeviewSelect>>', self.onSelectProdutos)
        self.atualizar_totais()

    def excluir_produto(self):
        lista_produtos = self.grid_produtos.tree.selection()[0]
        self.produtos_adicionados = [p for p in self.produtos_adicionados if p != lista_produtos]
        self.grid_produtos.remove_row()
        self.atualizar_totais()

    def editarPrProduto(self, event):
        nova_porcentagem = self.entry_editar_pr_produto.get()
        lista_produtos = self.grid_produtos.tree.selection()[0]
        values = list(self.grid_produtos.tree.item(lista_produtos, 'values'))
        values[4] = nova_porcentagem
        self.grid_produtos.tree.item(lista_produtos, values=values)
        item_index = self.grid_produtos.tree.index(lista_produtos)
        produto_atual = self.produtos_adicionados[item_index]
        self.produtos_adicionados[item_index] = (produto_atual[0], produto_atual[1], produto_atual[2],  produto_atual[3], nova_porcentagem)
        self.atualizar_totais()

    def editarQtdProduto(self, event):
        nova_quantidade = self.entry_editar_qtd_produto.get()
        lista_produtos = self.grid_produtos.tree.selection()[0]
        values = list(self.grid_produtos.tree.item(lista_produtos, 'values'))
        values[2] = nova_quantidade
        self.grid_produtos.tree.item(lista_produtos, values=values)
        item_index = self.grid_produtos.tree.index(lista_produtos)
        produto_atual = self.produtos_adicionados[item_index]
        self.produtos_adicionados[item_index] = (produto_atual[0], produto_atual[1], nova_quantidade, produto_atual[3], produto_atual[4])
        self.atualizar_totais()

    def atualizar_totais(self):
        total_quantidade = sum(int(produto[2]) for produto in self.produtos_adicionados)
        total_valor = 0
        for produto in self.produtos_adicionados:
            quantidade = int(produto[2])
            valor_unitario = float(produto[3])
            desconto = float(produto[4]) / 100  # Converte a porcentagem de desconto para um valor decimal
            valor_com_desconto = valor_unitario * (1 - desconto)
            total_valor += valor_com_desconto * quantidade
        
        self.label_total_itens.config(text=f"Total de Itens: {len(self.produtos_adicionados)}")
        self.label_total_quantidade.config(text=f"Total de Produtos: {total_quantidade}")
        self.label_total_valor.config(text=f"Valor Total: {locale.currency(total_valor, grouping=True)}")

    def onSelectProdutos(self, event):
        if self.grid_produtos.tree.selection():
            self.btn_excluir_produto.config(state=tk.NORMAL)
            self.entry_editar_pr_produto.config(state=tk.NORMAL)
            self.entry_editar_qtd_produto.config(state=tk.NORMAL)
            selected_item = self.grid_produtos.tree.selection()[0]
            # Pega os valores da linha selecionada
            values = self.grid_produtos.tree.item(selected_item, 'values')
            self.entry_editar_qtd_produto.delete(0, tk.END)
            self.entry_editar_qtd_produto.insert(0, values[2])
            self.entry_editar_pr_produto.delete(0, tk.END)
            self.entry_editar_pr_produto.insert(0, values[4])
        else:
            self.btn_excluir_produto.config(state=tk.DISABLED)
            self.entry_editar_pr_produto.config(state=tk.DISABLED)
            self.entry_editar_qtd_produto.config(state=tk.DISABLED)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()