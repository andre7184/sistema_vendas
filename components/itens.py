import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from components.cores import obter_cor

# Função para criar títulos
def criar_titulo(master, texto, componente, fonte=("Arial", 16), pady=None, padx=None):
    cor = obter_cor(componente, "titulo")
    label = tk.Label(master, text=texto, font=fonte, fg=cor)
    label.pack(pady=pady, padx=padx)
    return label

# Função para criar textos
def criar_texto(master, texto, componente, fonte=("Arial", 12), pady=5, padx=5, lado=tk.LEFT):
    cor = obter_cor(componente, "texto")
    label = tk.Label(master, text=texto, font=fonte, fg=cor)
    label.pack(pady=pady, padx=padx,side=lado)
    return label

# Função para criar entradas de texto
def criar_input(master, componente, largura=40, estado=tk.NORMAL, callback=None, textvariable=None, padx=None, pady=None, lado=None):
    entry = tk.Entry(master, width=largura, state=estado, textvariable=textvariable)
    entry.pack(pady=pady, padx=padx, side=lado)
    if callback:
        entry.bind("<Return>", callback)  # Chama a função callback ao pressionar Enter
    return entry

# Função para criar botões
def criar_botao(master, texto, comando, componente, estado=tk.NORMAL, largura=20, altura=1, lado=None, padx=None, pady=None):
    button = tk.Button(master, text=texto, command=comando, width=largura, height=altura, state=estado)
    button.pack(side=lado, padx=padx, pady=pady)
    return button

def criar_select(master, opcoes, componente, largura=37, estado=None, lado=None, padx=None, pady=None):
    variable = tk.StringVar(master)
    variable.set(opcoes[0] if opcoes else '')
    option_menu = tk.OptionMenu(master, variable, *opcoes)
    option_menu.config(width=largura)
    option_menu.pack(pady=pady, padx=padx, side=lado, fill=tk.X)
    
    # Ajusta o estado do menu
    menu = option_menu.nametowidget(option_menu.menuname)
    if estado == tk.DISABLED:
        menu.entryconfig(tk.END, state=tk.DISABLED)
    else:
        menu.entryconfig(tk.END, state=tk.NORMAL)
    
    return option_menu, variable

# Função para criar radio buttons
def criar_radio(master, texto, variable, valor, componente, comando=None, estado=tk.NORMAL, lado=None, padx=5, pady=5):
    radio = tk.Radiobutton(master, text=texto, variable=variable, value=valor, command=comando, state=estado)
    radio.pack(padx=padx, pady=pady, side=lado)
    return radio

# Função para criar frames
def criar_frame(master, componente, lado=tk.TOP, preencher=None, expandir=None, padding=0, anchor=None):
    cor_fundo = obter_cor(componente, "fundo")
    if cor_fundo:
        frame = tk.Frame(master, bg=cor_fundo)
    else:
        frame = tk.Frame(master)
    frame.pack(side=lado, fill=preencher, expand=expandir, padx=padding, pady=padding, anchor=anchor)
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

def criar_frame_com_scroll(root):
    # Frame principal com cor de fundo, borda e relevo
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Canvas para adicionar as barras de rolagem
    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de rolagem vertical
    v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configuração da barra de rolagem no Canvas
    canvas.configure(yscrollcommand=v_scrollbar.set)

    # Frame secundário dentro do Canvas
    second_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # Ajuste da região de rolagem do Canvas conforme o Frame secundário é redimensionado
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Define o tamanho mínimo da janela com base apenas na largura do conteúdo
        root.update_idletasks()
        root.minsize(second_frame.winfo_reqwidth(), 1)  # 1 é o valor mínimo para a altura

        # Verifica se o conteúdo é maior que a janela antes de ajustar a região de rolagem
        if second_frame.winfo_reqheight() > canvas.winfo_height():
            canvas.configure(scrollregion=canvas.bbox("all"))
        else:
            canvas.configure(scrollregion=(0, 0, second_frame.winfo_reqwidth(), canvas.winfo_height()))

    second_frame.bind("<Configure>", on_frame_configure)

    # Ajuste a largura do second_frame para preencher o Canvas
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas_window = canvas.create_window((0, 0), window=second_frame, anchor="nw")
    canvas.bind("<Configure>", on_canvas_configure)

    # Vincula o evento de rolagem do mouse ao Canvas
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    return main_frame, second_frame



# Função para ajustar a largura das colunas de uma Treeview
def adjust_column_width(tree):
    tree.update_idletasks()  # Atualiza a interface para garantir que o conteúdo seja renderizado
    for col in tree['columns']:
        max_width = tkFont.Font().measure(tree.heading(col)['text'])
        for item in tree.get_children():
            cell_text = tree.set(item, col)
            cell_width = tkFont.Font().measure(cell_text)
            if cell_width > max_width:
                max_width = cell_width
        tree.column(col, width=max_width)
