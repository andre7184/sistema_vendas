import tkinter as tk
from tkinter import ttk

def criar_frame_com_scroll(root):
    # Frame principal com cor de fundo, borda e relevo
    main_frame = tk.Frame(root, bg="blue")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Canvas para adicionar as barras de rolagem
    canvas = tk.Canvas(main_frame, background="violet")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de rolagem vertical
    v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configuração da barra de rolagem no Canvas
    canvas.configure(yscrollcommand=v_scrollbar.set)

    # Frame secundário dentro do Canvas
    second_frame = tk.Frame(canvas, background="red")
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

# Exemplo de uso
root = tk.Tk()
main_frame, second_frame = criar_frame_com_scroll(root)

# Adiciona widgets ao frame secundário
tk.Label(second_frame, text="Conteúdo do Frame Secundário").pack(padx=10, pady=10)

for i in range(10):
    tk.Label(second_frame, text=f"Item {i}").pack(padx=10, pady=5)

# Inicia o loop principal
root.mainloop()