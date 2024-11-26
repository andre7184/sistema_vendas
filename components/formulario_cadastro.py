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
        for campo in self.campos:
            label = tk.Label(self, text=campo)
            label.pack()
            entry = tk.Entry(self)
            entry.pack()
            self.entries[campo] = entry

        self.button_salvar = tk.Button(self, text="Salvar", command=self.salvar_dados)
        self.button_salvar.pack()

    def salvar_dados(self):
        dados = {campo: entry.get() for campo, entry in self.entries.items()}
        self.salvar_callback(dados)