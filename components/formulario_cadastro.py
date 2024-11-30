import tkinter as tk
from components.itens import criar_texto, criar_input, criar_botao, criar_select, criar_mensagem
from components.cores import obter_cor

class FormularioCadastro(tk.Frame):
    def __init__(self, master, campos, salvar_callback):
        super().__init__(master)
        self.salvar_callback = salvar_callback
        self.campos = campos
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        self.variables = {}  # Dicionário para armazenar as variáveis dos OptionMenus
        self.mensagem_label = criar_mensagem(self, "FormularioCadastro", texto="", tipo="erro")
        
        for campo, config in self.campos.items():
            criar_texto(self, campo, "FormularioCadastro")
            if config["tipo"] == "entry":
                self.entries[campo] = criar_input(self, "FormularioCadastro")
            elif config["tipo"] == "password":
                self.entries[campo] = criar_input(self, "FormularioCadastro")
                self.entries[campo].config(show="*")
            elif config["tipo"] == "select":
                self.entries[campo], self.variables[campo] = criar_select(self, config["options"], "FormularioCadastro")
            elif config["tipo"] == "integer":
                self.entries[campo] = criar_input(self, "FormularioCadastro")
                self.entries[campo].config(validate="key", validatecommand=(self.register(self.validate_inteiro), '%P'))
            elif config["tipo"] == "real":
                self.entries[campo] = criar_input(self, "FormularioCadastro")
                self.entries[campo].bind("<FocusOut>", self.formatar_real)

        criar_botao(self, "Salvar", self.salvar_dados, "FormularioCadastro", altura=2, lado=tk.TOP)

    def validate_inteiro(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def formatar_real(self, event):
        entry = event.widget
        value = entry.get().replace(',', '').replace('.', '')
        if value.isdigit():
            value = f'{int(value):,}'
            value = value.replace(',', '.')
            if len(value) > 2:
                value = value[:-2] + ',' + value[-2:]
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.icursor(len(value))

    def salvar_dados(self):
        dados = {}
        for campo, widget in self.entries.items():
            if isinstance(widget, tk.Entry):
                dados[campo] = widget.get()
            elif isinstance(widget, tk.OptionMenu):
                dados[campo] = self.variables[campo].get()
        self.salvar_callback(dados)

    def set_dados(self, dados):
        for campo, valor in dados.items():
            widget = self.entries.get(campo)
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, valor)
            elif isinstance(widget, tk.OptionMenu):
                self.variables[campo].set(valor)

    def mostrar_mensagem(self, mensagem, tipo):
        self.mensagem_label.config(text=mensagem, fg=obter_cor("FormularioCadastro", tipo))