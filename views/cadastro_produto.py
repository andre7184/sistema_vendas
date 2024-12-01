import tkinter as tk
from components.formulario_cadastro import FormularioCadastro
from components.itens import criar_titulo

class CadastroProduto(tk.Frame):
    def __init__(self, master, produto_controller, produto=None):
        super().__init__(master)
        self.produto_controller = produto_controller
        self.produto = produto
        campos = {
            "Nome": {"tipo": "entry"},
            "Descrição": {"tipo": "entry"},
            "Quantidade": {"tipo": "integer"},
            "Valor": {"tipo": "real"}
        }
        self.titulo = criar_titulo(self, "Cadastrar Produto", "CadastroProduto", fonte=("Arial", 16), pady=5)
        self.formulario = FormularioCadastro(self, campos, self.salvar_produto)
        
        
        if produto:
            self.preencher_dados(produto)
            self.titulo.config(text="Editar Produto")

    def preencher_dados(self, produto):
        self.formulario.set_dados({
            "Nome": produto.nome,
            "Descrição": produto.descricao,
            "Quantidade": produto.quantidade,
            "Valor": produto.valor
        })

    def salvar_produto(self, dados):
        nome = dados["Nome"]
        descricao = dados["Descrição"]
        quantidade = int(dados["Quantidade"])
        valor = float(dados["Valor"])
        try:
            if self.produto:
                self.produto_controller.atualizar_usuario(self.produto.id, nome, descricao, quantidade, valor)
                mensagem = "Produto atualizado com sucesso!"
            else:
                self.produto_controller.cadastrar_usuario(nome, descricao, quantidade, valor)
                mensagem = "Produto cadastrado com sucesso!"
            self.master.atualizar_lista()
            self.master.mostrar_mensagem(mensagem, "sucesso")
        except Exception as e:
            mensagem = f"Erro ao salvar Produto: {str(e)}"
            self.formulario.mostrar_mensagem(mensagem, "erro")
