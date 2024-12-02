import tkinter as tk
from tkinter import ttk
from components.itens import criar_input, criar_select, criar_texto, criar_titulo, criar_mensagem, criar_botao, criar_frame
from components.cores import obter_cor
from components.grid import Grid

class RelatorioVendas(tk.Frame):
    def __init__(self, master, venda_controller, usuario_controller, cliente_controller, produto_controller):
        super().__init__(master)
        self.master = master
        self.venda_controller = venda_controller
        self.cliente_controller = cliente_controller
        self.produto_controller = produto_controller
        self.usuario_controller = usuario_controller
        self.modo_visualizacao = master.current_user.get_tipo() == "Vendedor"

        # Inicializar variáveis para OptionMenu
        self.ano_inicial_var = tk.StringVar(self)
        self.mes_inicial_var = tk.StringVar(self)
        self.ano_final_var = tk.StringVar(self)
        self.mes_final_var = tk.StringVar(self)
        
        # Inicializar widgets de busca
        self.vendedor_entry = tk.Entry(self)
        self.cliente_entry = tk.Entry(self)

        self.showGrid()

    def showGrid(self):
        self.pack(fill=tk.BOTH, expand=True)
        colunas = ["ID", "Cliente", "Vendedor", "Produtos", "Valor Total", "Data"]
        self.dados = self.obter_dados_vendas()
        
        self.titulo = criar_titulo(self, "Relatório de Vendas", "RelatorioVendas", fonte=("Arial", 16), pady=5)
        self.mensagem_label = criar_mensagem(self, "RelatorioVendas", "", tipo="sucesso")
        self.frame_busca_datas = criar_frame(self, "RelatorioVendas", lado=tk.TOP)
        
        # Widgets de busca
        datas = [venda[5] for venda in self.dados]
        anos = sorted(set([data.split('-')[0] for data in datas]), reverse=True) or [""]
        meses = [f"{i:02d}" for i in range(1, 13)]
        self.data_inicial_label = criar_texto(self.frame_busca_datas, "Data Inicial:", "RelatorioVendas", lado=tk.LEFT, padx=5)
        self.ano_inicial_menu, self.ano_inicial_var = criar_select(self.frame_busca_datas, anos, self.ano_inicial_var, lado=tk.LEFT, padx=5)
        self.mes_inicial_menu, self.mes_inicial_var = criar_select(self.frame_busca_datas, meses, self.mes_inicial_var, lado=tk.LEFT, padx=5)
        self.data_final_label = criar_texto(self.frame_busca_datas, "Data Final:", "RelatorioVendas", lado=tk.LEFT)
        self.ano_final_menu, self.ano_final_var = criar_select(self.frame_busca_datas, anos, self.ano_final_var, lado=tk.LEFT, padx=5)
        self.mes_final_menu, self.mes_final_var = criar_select(self.frame_busca_datas, meses, self.mes_final_var, lado=tk.LEFT, padx=5)
        self.frame_busca_nome = criar_frame(self, "RelatorioVendas", lado=tk.TOP)
        self.vendedor_label = criar_texto(self.frame_busca_nome, "Vendedor:", "RelatorioVendas", lado=tk.LEFT)
        self.vendedor_entry = criar_input(self.frame_busca_nome, "RelatorioVendas", lado=tk.LEFT, padx=5)
        self.cliente_label = criar_texto(self.frame_busca_nome, "Cliente:", "RelatorioVendas", lado=tk.LEFT)
        self.cliente_entry = criar_input(self.frame_busca_nome, "RelatorioVendas", lado=tk.LEFT, padx=5)
        self.frame_busca_botoes = criar_frame(self, "RelatorioVendas", lado=tk.TOP)
        self.btn_buscar = criar_botao(self.frame_busca_botoes, "Buscar", self.buscar_vendas, "RelatorioVendas", altura=1, lado=tk.LEFT, padx=5, pady=5)
        self.btn_atualizar = criar_botao(self.frame_busca_botoes, "Atualizar", self.atualizar_lista, "RelatorioVendas", altura=1, lado=tk.LEFT, padx=5, pady=5)
        
        if not self.modo_visualizacao:
            self.btn_exportar = criar_botao(self.frame_busca_botoes, "Exportar", self.exportar_relatorio, "RelatorioVendas", altura=1, lado=tk.LEFT, padx=5, pady=5)
        
        self.lista_vendas = Grid(self, colunas, self.dados)

    def obter_dados_vendas(self):
        dados = []
        datas = []
        for venda in self.venda_controller.listar_vendas():
            if self.modo_visualizacao and venda.vendedor_id != self.master.current_user.get_id():
                continue
            relatorio = venda.gerar_relatorio(self.cliente_controller, self.usuario_controller)
            dados.append((
                relatorio['id'],
                relatorio['cliente'],
                relatorio['vendedor'],
                ', '.join(map(str, relatorio['produtos'])),
                relatorio['valor_total'],
                relatorio['data_venda']
            ))
            datas.append(relatorio['data_venda'])
        
        if datas:
            anos = sorted(set([data.split('-')[0] for data in datas]), reverse=True)
            meses = [f"{i:02d}" for i in range(1, 13)]
            
            if anos:
                self.ano_inicial_var.set(min(anos))
                self.ano_final_var.set(max(anos))
            if meses:
                self.mes_inicial_var.set("01")
                self.mes_final_var.set("12")
        else:
            anos = [""]
            self.ano_inicial_var.set("")
            self.ano_final_var.set("")
            self.mes_inicial_var.set("01")
            self.mes_final_var.set("12")
        
        return dados

    def atualizar_lista(self):
        self.clear_frame()
        self.showGrid()

    def buscar_vendas(self):
        ano_inicial = self.ano_inicial_var.get()
        mes_inicial = self.mes_inicial_var.get()
        data_inicial = f"{ano_inicial}-{mes_inicial}-01"
        
        ano_final = self.ano_final_var.get()
        mes_final = self.mes_final_var.get()
        data_final = f"{ano_final}-{mes_final}-31"
        
        vendedor = self.vendedor_entry.get().lower()
        cliente = self.cliente_entry.get().lower()
        
        dados_filtrados = []
        for venda in self.dados:
            data_venda = venda[5]
            nome_vendedor = venda[2].lower()
            nome_cliente = venda[1].lower()
            
            if (not data_inicial or data_venda >= data_inicial) and \
            (not data_final or data_venda <= data_final) and \
            (not vendedor or vendedor in nome_vendedor) and \
            (not cliente or cliente in nome_cliente):
                dados_filtrados.append(venda)
        
        self.lista_vendas.atualizar_dados(dados_filtrados)

    def exportar_relatorio(self):
        caminho_arquivo = "relatorio_vendas.csv"  # Defina o caminho do arquivo CSV
        dados = self.lista_vendas.obter_dados()
        self.venda_controller.exportar_relatorio_csv(caminho_arquivo, dados)
        self.mostrar_mensagem(f"Relatório exportado para {caminho_arquivo}", "sucesso")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def mostrar_mensagem(self, mensagem, tipo):
        self.mensagem_label.config(text=mensagem, fg=obter_cor("RelatorioVendas", tipo))