import tkinter as tk
from components.formulario_cadastro import FormularioCadastro
from components.itens import criar_titulo

class CadastroCliente(tk.Frame):
    def __init__(self, master, cliente_controller, cliente=None, janela=None):
        super().__init__(master)
        self.cliente_controller = cliente_controller
        self.cliente = cliente
        self.janela = janela
        campos = {
            "Nome": {"tipo": "entry"},
            "CPF": {"tipo": "entry"},
            "Endereço": {"tipo": "entry"}
        }
        self.titulo = criar_titulo(self, "Cadastrar Cliente", "CadastroCliente", fonte=("Arial", 16), pady=5)
        self.formulario = FormularioCadastro(self, campos, self.salvar_cliente)
        
        if cliente:
            self.preencher_dados(cliente)
            self.titulo.config(text="Editar Cliente")

    def preencher_dados(self, cliente):
        self.formulario.set_dados({
            "Nome": cliente.nome,
            "CPF": cliente.cpf,
            "Endereço": cliente.endereco
        })

    def salvar_cliente(self, dados):
        nome = dados["Nome"]
        cpf = dados["CPF"]
        endereco = dados["Endereço"]
        
        try:
            if self.cliente:
                self.cliente_controller.atualizar_cliente(self.cliente.id, nome, cpf, endereco)
                mensagem = "Cliente atualizado com sucesso!"
            else:
                self.cliente_controller.cadastrar_cliente(nome, cpf, endereco)
                mensagem = "Cliente cadastrado com sucesso!"
            if self.janela:
                self.janela.atualizarClientesSelecionado({'id': self.cliente.id, 'nome': nome, 'cpf': cpf, 'endereco': endereco})
                self.destroy()
                self.master.destroy()
            else:
                self.master.atualizar_lista()
                self.master.mostrar_mensagem(mensagem, "sucesso")
        except Exception as e:
            mensagem = f"Erro ao salvar cliente: {str(e)}"
            self.formulario.mostrar_mensagem(mensagem, "erro")