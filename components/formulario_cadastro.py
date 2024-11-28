import tkinter as tk

class FormularioCadastro(tk.Frame):
    def __init__(self, master, campos, salvar_callback):
        super().__init__(master)
        self.salvar_callback = salvar_callback
        self.campos = campos
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.entries = {}
        self.mensagem_label = tk.Label(self, text="", fg="red")
        self.mensagem_label.pack(pady=10)
        for campo, config in self.campos.items():
            label = tk.Label(self, text=campo)
            label.pack(pady=5)
            widget = self.create_widget(config)
            widget.pack(pady=5, padx=10, fill=tk.X)
            self.entries[campo] = widget

        self.button_salvar = tk.Button(self, text="Salvar", command=self.salvar_dados, width=20, height=2)
        self.button_salvar.pack(pady=10)

    def create_widget(self, config):
        tipo = config.get('tipo', 'entry')
        if tipo == 'entry':
            return tk.Entry(self, width=40)
        elif tipo == 'password':
            return tk.Entry(self, show='*', width=40)
        elif tipo == 'select':
            options = config.get('options', [])
            variable = tk.StringVar(self)
            variable.set(options[0] if options else '')
            option_menu = tk.OptionMenu(self, variable, *options)
            option_menu.config(width=37)
            option_menu.variable = variable
            return option_menu
        elif tipo == 'integer':
            return tk.Entry(self, validate="key", validatecommand=(self.register(self.validate_inteiro), '%P'), width=40)
        elif tipo == 'real':
            return tk.Entry(self, width=40)
        return tk.Entry(self)

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
                dados[campo] = widget.variable.get()
        self.salvar_callback(dados)

    def set_dados(self, dados):
        for campo, valor in dados.items():
            widget = self.entries.get(campo)
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, valor)
            elif isinstance(widget, tk.OptionMenu):
                widget.variable.set(valor)

    def mostrar_mensagem(self, mensagem, tipo):
        if tipo == "sucesso":
            self.mensagem_label.config(text=mensagem, fg="green")
        else:
            self.mensagem_label.config(text=mensagem, fg="red")