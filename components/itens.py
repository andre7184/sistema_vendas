import tkinter as tk
from tkinter import ttk
from components.cores import obter_cor

# Função para criar títulos
def criar_titulo(master, texto, componente, fonte=("Arial", 16)):
    cor = obter_cor(componente, "titulo")
    label = tk.Label(master, text=texto, font=fonte, fg=cor)
    label.pack(pady=5)
    return label

# Função para criar textos
def criar_texto(master, texto, componente, fonte=("Arial", 12)):
    cor = obter_cor(componente, "texto")
    label = tk.Label(master, text=texto, font=fonte, fg=cor)
    label.pack(pady=5)
    return label

# Função para criar entradas de texto
def criar_input(master, componente, largura=40, estado=tk.NORMAL, callback=None):
    entry = tk.Entry(master, width=largura, state=estado)
    entry.pack(pady=5, padx=10, fill=tk.X)
    if callback:
        entry.bind("<Return>", callback)  # Chama a função callback ao pressionar Enter
    return entry

# Função para criar botões
def criar_botao(master, texto, comando, componente, largura=20, altura=1, lado=tk.LEFT, padx=5, pady=5):
    button = tk.Button(master, text=texto, command=comando, width=largura, height=altura)
    button.pack(side=lado, padx=padx, pady=pady)
    return button

# Função para criar selects (OptionMenu)
def criar_select(master, opcoes, componente, largura=37):
    variable = tk.StringVar(master)
    variable.set(opcoes[0] if opcoes else '')
    option_menu = tk.OptionMenu(master, variable, *opcoes)
    option_menu.config(width=largura)
    option_menu.pack(pady=5, padx=10, fill=tk.X)
    return option_menu, variable

# Função para criar radio buttons
def criar_radio(master, texto, variable, valor, componente, comando=None):
    radio = tk.Radiobutton(master, text=texto, variable=variable, value=valor, command=comando)
    radio.pack(side=tk.LEFT, padx=5)
    return radio

# Função para criar frames
def criar_frame(master, componente, lado=tk.TOP, preencher=tk.BOTH, expandir=True, padding=10):
    frame = tk.Frame(master, bg=obter_cor(componente, "fundo"))
    frame.pack(side=lado, fill=preencher, expand=expandir, padx=padding, pady=padding)
    return frame

# Função para criar barras de rolagem
def criar_scroll(master, componente, orientacao=tk.VERTICAL, comando=None):
    scrollbar = tk.Scrollbar(master, orient=orientacao, command=comando)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    return scrollbar

# Função para criar janelas
def criar_janela(titulo="Nova Janela", largura=400, altura=300):
    janela = tk.Toplevel()
    janela.title(titulo)
    janela.geometry(f"{largura}x{altura}")
    return janela

# Função para criar Treeview (grid)
def criar_treeview(master, colunas, componente, altura=10):
    tree = ttk.Treeview(master, columns=colunas, show='headings', height=altura)
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True)
    return tree

# Função para criar mensagens de erro/sucesso
def criar_mensagem(master, componente, texto="", tipo="erro"):
    cor = obter_cor(componente, tipo)
    label = tk.Label(master, text=texto, fg=cor)
    label.pack(pady=1)
    return label

# Função para criar labels dinâmicos
def criar_label_dinamico(master, componente, texto="", fonte=("Arial", 10)):
    label = tk.Label(master, text=texto, font=fonte)
    label.pack(side=tk.LEFT, padx=5)
    return label