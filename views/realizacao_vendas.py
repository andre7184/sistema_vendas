import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from components.grid import Grid
from components.itens import criar_botao, criar_frame, criar_input, criar_radio, criar_texto, criar_titulo
from views.cadastro_cliente import CadastroCliente
from components.scroll import ScrollableFrame
import locale

# Configura o locale para o formato de moeda brasileira
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
class RealizacaoVendas(tk.Frame):
    def __init__(self, parent, master, venda_controller, cliente_controller, produto_controller):
        super().__init__(master)
        self.parent = parent
        self.venda_controller = venda_controller
        self.produto_controller = produto_controller
        self.cliente_controller = cliente_controller
        self.produtos_adicionados = []
        self.colunas_produtos_adicionados = ["ID", "Nome", "Qtd", "Valor Unitário", "Desconto", "Valor Total"]
        self.cliente_selecionado = {}
        self.grid_clientes = None
        self.forma_pagamento = tk.StringVar(value="À vista")
        self.parcelas = tk.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):
        #self.pack(fill=tk.BOTH, expand=True, padx=0, pady=0, anchor="n")
        self.frame_venda = self #criar_frame(self,RealizacaoVendas, preencher=tk.X, expandir=True, anchor="n")
        self.label_titulo = criar_titulo(self.frame_venda, "Realizar Venda", RealizacaoVendas, pady=5)
        self.frame_cliente = self.create_section(self.frame_venda, "Cliente", self.buscar_dados_cliente)
        self.grid_clientes = self.create_lista_clientes(self.frame_venda)
        self.frame_dados_cliente = self.create_dados_cliente(self.frame_venda)
        self.frame_produtos = self.create_section(self.frame_venda, "Produto", self.buscar_dados_produto, tk.DISABLED)
        self.grid_produtos = Grid(self.frame_venda, ["ID", "Nome", "Quantidade", "Valor"], [], 3)
        self.grid_produtos.pack(pady=5, fill=tk.X, expand=True)
        self.frame_adicionar_produto = self.create_adicionar_produto(self.frame_venda)
        self.frame_produtos_adicionados = criar_frame(self.frame_venda, RealizacaoVendas, preencher=tk.X, expandir=True)
        self.grid_produtos_adicionados = self.criarSecaoProdutosAdicionados([])
        self.total_frame = self.create_total_frame(self.frame_venda)
        self.frame_finalizar_venda = self.createFinalizarVenda(self.frame_venda)

    def create_lista_clientes(self,parent):
        if self.grid_clientes:
            self.grid_clientes.pack_forget()  # Esconde a grid existente
        grid = Grid(parent, ["ID", "Nome", "CPF", "Endereço"], [], 3)
        grid.pack(after=self.frame_cliente, pady=5, fill=tk.BOTH, expand=True)
        grid.tree.bind('<<TreeviewSelect>>', self.onSelectClientes)
        return grid

    def create_section(self, parent, label_text, callback, state=tk.NORMAL):
        frame = criar_frame(parent, RealizacaoVendas, padding=5, preencher=tk.X, expandir=True) #tk.Frame(parent)
        label, entry = self.addFrameBuscar(frame, label_text, state, callback)
        setattr(self, f"entry_buscar_{label_text.lower()}", entry)  # Armazena a referência do campo de entrada
        return frame

    def create_dados_cliente(self, parent):
        frame = criar_frame(parent, RealizacaoVendas, padding=5, preencher=tk.X, expandir=True)
        self.label_dados_cliente = criar_texto(frame, "", RealizacaoVendas, lado=tk.LEFT) #tk.Label(frame, text="", font=("Arial", 10))
        self.btn_editar_cliente = criar_botao(frame, "Editar Cliente", self.editar_cliente, RealizacaoVendas, lado=tk.LEFT)    #tk.Button(frame, text="Editar Cliente", command=self.editar_cliente)
        return frame

    def create_adicionar_produto(self, parent):
        frame = criar_frame(parent, RealizacaoVendas, padding=5, preencher=tk.X, expandir=True)
        self.entry_quantidade = criar_input(frame, RealizacaoVendas, largura=5, lado=tk.LEFT) #tk.Entry(frame, width=5, state=tk.NORMAL)
        self.entry_quantidade.insert(0, 1)
        self.entry_quantidade.configure(state=tk.DISABLED)
        self.btn_adicionar_produto = criar_botao(frame, "Adicionar Produto", self.adicionar_produto, RealizacaoVendas, estado=tk.DISABLED, lado=tk.LEFT) #tk.Button(frame, text="Adicionar Produto", command=self.adicionar_produto, state=tk.DISABLED)
        return frame

    def criarSecaoProdutosAdicionados(self, dados=[]):
        self.frame_editar_produto = criar_frame(self.frame_produtos_adicionados, RealizacaoVendas, padding=5, preencher=tk.X, expandir=True) #tk.Frame(self.frame_produtos_adicionados)
        self.btn_excluir_produto = criar_botao(self.frame_editar_produto, "Excluir Produto", self.excluir_produto, RealizacaoVendas, lado=tk.LEFT) #tk.Button(self.frame_editar_produto, text="Excluir Produto", state=tk.DISABLED, command=self.excluir_produto)
        self.entry_editar_qtd_produto = self.createEditProdutos(self.frame_editar_produto, "Editar Quantidade:", width=5, function_callback=self.editarQtdProduto)
        self.entry_editar_pr_produto = self.createEditProdutos(self.frame_editar_produto, "Editar Porcentagem de Desconto:", width=5, function_callback=self.editarPrProduto)
        grid_produtos_adicionados = Grid(self.frame_produtos_adicionados, self.colunas_produtos_adicionados, dados, 3)
        grid_produtos_adicionados.pack(pady=5, fill=tk.BOTH, expand=True)
        grid_produtos_adicionados.tree.bind('<<TreeviewSelect>>', self.onSelectProdutos)
        return grid_produtos_adicionados

    def create_total_frame(self, parent):
        frame = criar_frame(parent, RealizacaoVendas, padding=5, preencher=tk.X, expandir=True)
        self.label_total_itens = criar_texto(frame, "Total de Itens: 0", RealizacaoVendas, lado=tk.LEFT, padx=5) #tk.Label(frame, text="Total de Itens: 0")
        self.label_total_quantidade = criar_texto(frame, "Total de Produtos: 0", RealizacaoVendas, lado=tk.LEFT, padx=5) #tk.Label(frame, text="Total de Produtos: 0")
        self.label_total_valor = criar_texto(frame, "Valor Total: 0.00", RealizacaoVendas, lado=tk.LEFT, padx=5) #tk.Label(frame, text="Valor Total: 0.00")
        return frame

    def createEditProdutos(self, frame, texto, width=10, function_callback=None):
        label_editar_produto = criar_texto(frame, texto, RealizacaoVendas, lado=tk.LEFT, padx=5) #tk.Label(frame, text=texto, font=("Arial", 10))
        entry_editar_produto = criar_input(frame, RealizacaoVendas, estado=tk.DISABLED, largura=5, lado=tk.LEFT) #tk.Entry(frame, state=tk.DISABLED, width=width) 
        entry_editar_produto.bind("<KeyRelease>", function_callback)
        return entry_editar_produto

    def addFrameBuscar(self, frame, texto, state, callback):
        label = criar_texto(frame, texto, RealizacaoVendas, lado=tk.LEFT, padx=5) #tk.Label(frame, text=texto, font=("Arial", 14))
        entry = criar_input(frame, RealizacaoVendas, estado=state, largura=50, lado=tk.LEFT) #tk.Entry(frame, state=state, width=50) 
        entry.bind("<KeyRelease>", callback)
        return label, entry 

    def createFinalizarVenda(self, parent):
        frame = criar_frame(parent, RealizacaoVendas, padding=5, preencher=tk.X, expandir=True)
        self.label_pagamento = criar_texto(frame, "Forma de Pagamento:", RealizacaoVendas, lado=tk.LEFT, padx=5) #tk.Label(self.frame, text="Forma de Pagamento:", font=("Arial", 14))
        self.radio_avista = criar_radio(frame, "À vista", self.forma_pagamento, "À vista", RealizacaoVendas, estado=tk.DISABLED, comando=self.toggle_parcelas, lado=tk.LEFT) #tk.Radiobutton(self.frame, text="À vista", variable=self.forma_pagamento, value="À vista", state=tk.DISABLED, command=self.toggle_parcelas)
        self.radio_parcelado = criar_radio(frame, "Parcelado", self.forma_pagamento, "Parcelado", RealizacaoVendas, estado=tk.DISABLED, comando=self.toggle_parcelas, lado=tk.LEFT) #tk.Radiobutton(self.frame, text="Parcelado", variable=self.forma_pagamento, value="Parcelado", state=tk.DISABLED, command=self.toggle_parcelas)
        self.label_parcelas = criar_texto(frame, "Parcelas:", RealizacaoVendas, lado=tk.LEFT, padx=5) #tk.Label(self.frame, text="Parcelas:", font=("Arial", 14))
        self.entry_parcelas = criar_input(frame, RealizacaoVendas, largura=5, estado=tk.DISABLED,textvariable=self.parcelas, lado=tk.LEFT) #tk.Entry(self.frame, textvariable=self.parcelas, width=5, state=tk.DISABLED)
        self.btn_finalizar_venda = criar_botao(self.frame_venda, "Finalizar Venda", self.finalizar_venda, RealizacaoVendas, estado=tk.DISABLED, lado=tk.TOP, padx=15, pady=15) #tk.Button(self.frame, text="Finalizar Venda", state=tk.DISABLED, command=self.finalizar_venda)
        return frame

    def buscar_dados_cliente(self, event=None):
        nome_cliente = self.entry_buscar_cliente.get()
        clientes = self.cliente_controller.buscar_cliente_por_nome(nome_cliente)
        if clientes:
            dados_clientes = [(cliente.get_id(), cliente.get_nome(), cliente.get_cpf(), cliente.get_endereco()) for cliente in clientes]
            if not self.grid_clientes or not self.grid_clientes.winfo_ismapped():
                self.grid_clientes = self.create_lista_clientes(self.frame_venda)
                self.cliente_selecionado = {}
            self.grid_clientes.update_data(dados_clientes)
            # Limpar o texto da label_dados_cliente e desativar o botão btn_editar_cliente
            self.label_dados_cliente.config(text="")
            self.btn_editar_cliente.config(state=tk.DISABLED)
            self.entry_buscar_produto.config(state=tk.DISABLED)
            self.entry_quantidade.config(state=tk.DISABLED)
            self.btn_adicionar_produto.config(state=tk.DISABLED)

    def buscar_dados_produto(self, event=None):
        nome_produto = self.entry_buscar_produto.get()
        produtos = self.produto_controller.buscar_produto_por_nome(nome_produto)
        dados_produtos = [(produto.id, produto.nome, produto.quantidade, produto.valor) for produto in produtos]
        # Atualizar a grid de produtos
        self.grid_produtos.update_data(dados_produtos)

    def onSelectClientes(self, event):
        selected_items = self.grid_clientes.tree.selection()
        if not selected_items:
            return
        selected_item = selected_items[0]
        cliente_id = self.grid_clientes.tree.item(selected_item)['values'][0]
        cliente_nome = self.grid_clientes.tree.item(selected_item)['values'][1]
        cliente_cpf = self.grid_clientes.tree.item(selected_item)['values'][2]
        cliente_endereco = self.grid_clientes.tree.item(selected_item)['values'][3]
        self.cliente_selecionado = {'id': cliente_id, 'nome': cliente_nome, 'cpf': cliente_cpf, 'endereco': cliente_endereco}
        cliente_info = f"Nome: {cliente_nome}, Endereço: {cliente_endereco}"
        self.label_dados_cliente.config(text=cliente_info)
        self.btn_editar_cliente.config(state=tk.NORMAL)
        self.entry_buscar_produto.config(state=tk.NORMAL)
        self.entry_quantidade.config(state=tk.NORMAL)
        self.btn_adicionar_produto.config(state=tk.NORMAL)
        self.grid_clientes.pack_forget()

    def atualizarClientesSelecionado(self,clientes):
        self.cliente_selecionado = clientes
        cliente_info = f"Nome: {clientes['nome']}, Endereço: {clientes['endereco']}"
        self.label_dados_cliente.config(text=cliente_info)

    def editar_cliente(self):
        selected_item = self.grid_clientes.tree.selection()[0]
        cliente_id = self.grid_clientes.tree.item(selected_item)['values'][0]
        cliente_obj = self.cliente_controller.buscar_cliente_por_id(cliente_id)
        
        # Criar uma nova janela para edição do cliente
        nova_janela = tk.Toplevel(self.master)
        nova_janela.title("Editar Cliente")
        
        # Passar a nova janela como master para o CadastroCliente
        cadastro_cliente_frame = CadastroCliente(nova_janela, self.cliente_controller, cliente_obj, self)
        cadastro_cliente_frame.pack(fill=tk.BOTH, expand=True)

    def adicionar_produto(self):
        if self.grid_produtos.tree.selection():
            selected_item = self.grid_produtos.tree.selection()[0]
            produto_id = self.grid_produtos.tree.item(selected_item)['values'][0]
            produto_nome = self.grid_produtos.tree.item(selected_item)['values'][1]
            produto_valor = self.grid_produtos.tree.item(selected_item)['values'][3]
            quantidade = int(self.entry_quantidade.get())
            valor_total = quantidade * float(produto_valor)
            
            # Verifica se o produto já está na lista de produtos adicionados
            produto_existente = next((produto for produto in self.produtos_adicionados if produto[0] == produto_id), None)
            
            if produto_existente:
                # Atualiza a quantidade e o valor total do produto existente
                nova_quantidade = produto_existente[2] + quantidade
                # Verifica se o produto existente tem desconto aplicado
                if produto_existente[4] == 0:
                    novo_valor_total = nova_quantidade * float(produto_valor) 
                else:
                    novo_valor_total = float(nova_quantidade) * float(produto_valor) * (1 - float(produto_existente[4])/100)

                self.produtos_adicionados = [(produto_id, produto_nome, nova_quantidade, produto_valor, produto_existente[4], novo_valor_total) if produto[0] == produto_id else produto for produto in self.produtos_adicionados]
                # Atualiza a grade de produtos adicionados
                for item in self.grid_produtos_adicionados.tree.get_children():
                    if self.grid_produtos_adicionados.tree.item(item)['values'][0] == produto_id:
                        values = list(self.grid_produtos_adicionados.tree.item(item, 'values'))
                        values[2] = nova_quantidade
                        values[5] = novo_valor_total
                        self.grid_produtos_adicionados.tree.item(item, values=values)
                        break
            
            else:
                # Adiciona o novo produto à lista de produtos adicionados
                self.produtos_adicionados.append((produto_id, produto_nome, quantidade, produto_valor, 0, valor_total))
                # Atualiza a grade de produtos adicionados
                if hasattr(self, 'grid_produtos_adicionados'):
                    self.grid_produtos_adicionados.add_row((produto_id, produto_nome, quantidade, produto_valor, 0, valor_total))
                else:
                    self.atualizar_grid_produtos()
            
            # Atualiza os totais de itens e valores
            self.atualizar_totais()
            
            # Habilita a seção de forma de pagamento após adicionar o primeiro produto
            self.radio_avista.config(state=tk.NORMAL)
            self.radio_parcelado.config(state=tk.NORMAL)
            self.entry_parcelas.config(state=tk.NORMAL if self.forma_pagamento.get() == "Parcelado" else tk.DISABLED)
            self.btn_finalizar_venda.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Erro", "Selecione um produto para adicionar.")

    def atualizar_grid_produtos(self):
        dados = self.produtos_adicionados
        if hasattr(self, 'grid_produtos_adicionados'):
            self.grid_produtos_adicionados.destroy()

        # Frame para os botões
        self.grid_produtos_adicionados = self.criarSecaoProdutosAdicionados(dados)
        self.atualizar_totais()

    def excluir_produto(self):
        if self.grid_produtos_adicionados.tree.selection():
            selected_item = self.grid_produtos_adicionados.tree.selection()[0]
            produto_id = self.grid_produtos_adicionados.tree.item(selected_item)['values'][0]
            
            # Remove o produto da lista de produtos adicionados
            self.produtos_adicionados = [p for p in self.produtos_adicionados if p[0] != produto_id]
            
            # Remove o produto da grade de produtos adicionados
            self.grid_produtos_adicionados.tree.delete(selected_item)
            
            # Verifica se a lista de produtos adicionados está vazia
            if not self.produtos_adicionados or len(self.produtos_adicionados) == 0:
                self.radio_avista.config(state=tk.DISABLED)
                self.radio_parcelado.config(state=tk.DISABLED)
                self.entry_parcelas.config(state=tk.DISABLED)
                self.btn_finalizar_venda.config(state=tk.DISABLED)
            
            # Atualiza os totais de itens e valores
            self.atualizar_totais()
        else:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")

    def editarPrProduto(self, event):
        nova_porcentagem = self.entry_editar_pr_produto.get()
        lista_produtos = self.grid_produtos_adicionados.tree.selection()[0]
        values = list(self.grid_produtos_adicionados.tree.item(lista_produtos, 'values'))
        values[4] = nova_porcentagem
        # atualiza o valor total
        valor_total =   float(values[3]) * float(values[2]) * (1 - float(nova_porcentagem)/100) #values[2] * values[3] * (1 - float(nova_porcentagem)/100) 
        values[5] = valor_total
        self.grid_produtos_adicionados.tree.item(lista_produtos, values=values)
        item_index = self.grid_produtos_adicionados.tree.index(lista_produtos)
        produto_atual = self.produtos_adicionados[item_index]
        self.produtos_adicionados[item_index] = (produto_atual[0], produto_atual[1], produto_atual[2],  produto_atual[3], nova_porcentagem, valor_total)
        self.atualizar_totais()

    def editarQtdProduto(self, event):
        nova_quantidade = self.entry_editar_qtd_produto.get()
        lista_produtos = self.grid_produtos_adicionados.tree.selection()[0]
        values = list(self.grid_produtos_adicionados.tree.item(lista_produtos, 'values'))
        values[2] = nova_quantidade
        valor_total =  float(values[3]) * float(values[2]) * (1 - float(values[4])/100) #values[2] * values[3] * (1 - float(values[4])/100)
        values[5] = valor_total
        self.grid_produtos_adicionados.tree.item(lista_produtos, values=values)
        item_index = self.grid_produtos_adicionados.tree.index(lista_produtos)
        produto_atual = self.produtos_adicionados[item_index]
        self.produtos_adicionados[item_index] = (produto_atual[0], produto_atual[1], nova_quantidade, produto_atual[3], produto_atual[4], valor_total)
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
        if self.grid_produtos_adicionados.tree.selection():
            self.btn_excluir_produto.config(state=tk.NORMAL)
            self.entry_editar_pr_produto.config(state=tk.NORMAL)
            self.entry_editar_qtd_produto.config(state=tk.NORMAL)
            selected_item = self.grid_produtos_adicionados.tree.selection()[0]
            # Pega os valores da linha selecionada
            values = self.grid_produtos_adicionados.tree.item(selected_item, 'values')
            self.entry_editar_qtd_produto.delete(0, tk.END)
            self.entry_editar_qtd_produto.insert(0, values[2])
            self.entry_editar_pr_produto.delete(0, tk.END)
            self.entry_editar_pr_produto.insert(0, values[4])
        else:
            self.btn_excluir_produto.config(state=tk.DISABLED)
            self.entry_editar_pr_produto.config(state=tk.DISABLED)
            self.entry_editar_qtd_produto.config(state=tk.DISABLED)

    def toggle_parcelas(self):
        if self.forma_pagamento.get() == "Parcelado":
            self.entry_parcelas.config(state=tk.NORMAL)
        else:
            self.entry_parcelas.config(state=tk.DISABLED)

    def calcular_total(self):
        total_valor = 0
        for produto in self.produtos_adicionados:
            quantidade = int(produto[2])
            valor_unitario = float(produto[3])
            desconto = float(produto[4]) / 100
            valor_com_desconto = valor_unitario * (1 - desconto)
            total_valor += valor_com_desconto * quantidade
        return total_valor

    def limpar_venda(self):
        self.produtos_adicionados = []
        self.cliente_selecionado = {}
        self.grid_clientes = self.create_lista_clientes(self.frame_venda)
        self.grid_produtos.update_data([])
        self.atualizar_totais()
        self.label_dados_cliente.config(text="")
        self.btn_editar_cliente.config(state=tk.DISABLED)
        self.entry_buscar_produto.config(state=tk.DISABLED)
        self.entry_quantidade.config(state=tk.DISABLED)
        self.btn_adicionar_produto.config(state=tk.DISABLED)
        self.forma_pagamento.set("À vista")
        self.parcelas.set(1)
        self.radio_avista.config(state=tk.DISABLED)
        self.radio_parcelado.config(state=tk.DISABLED)
        self.entry_parcelas.config(state=tk.DISABLED)

    def finalizar_venda(self):
        if not self.produtos_adicionados or len(self.produtos_adicionados) == 0:
            messagebox.showerror("Erro", "Adicione produtos à venda antes de finalizar.")
            return

        forma_pagamento = self.forma_pagamento.get()
        parcelas = self.parcelas.get() if forma_pagamento == "Parcelado" else 1
        venda = {
            "cliente": self.cliente_selecionado,
            "vendedor": self.parent.current_user,
            "produtos": self.produtos_adicionados,
            "data": datetime.now().strftime("%Y-%m-%d"),
            "forma_pagamento": forma_pagamento,
            "parcelas": parcelas,
            "total": self.calcular_total()  
        }
        self.venda_controller.registrar_venda(venda)
        messagebox.showinfo("Sucesso", "Venda realizada com sucesso!")
        self.limpar_venda()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()