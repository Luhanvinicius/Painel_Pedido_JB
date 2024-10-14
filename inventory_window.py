import tkinter as tk
from tkinter import ttk

def open_inventory_window(root, conn, remessa):
    # Remover pontos da remessa para garantir que esteja no formato correto
    remessa_clean = remessa.replace('.', '')

    try:
        # Criar nova janela com o número da remessa no título
        new_window = tk.Toplevel(root)
        new_window.title(f"Consulta Inventário - Remessa: {remessa_clean}")

        # Criar frame para o Canvas
        container = tk.Frame(new_window)
        container.pack(fill="both", expand=True)

        # Adicionar Canvas e Scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configurar o Canvas para expandir com a janela
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Posicionar Canvas e Scrollbar na janela
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fazer o Canvas responder ao scroll do mouse
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

        # Associar o evento de scroll ao Canvas
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        # Executar a consulta SQL
        cursor = conn.cursor()
        query = """
        SELECT "DATA", "bipagem", "posição", "responsavel"
        FROM base_inventario_filiais
        WHERE remessa = %s
        """
        cursor.execute(query, (remessa_clean,))
        rows = cursor.fetchall()

        if rows:
            # Cria os cabeçalhos das colunas
            headers = ["DATA", "Bipagem", "Posição", "Responsável"]
            for col_num, header in enumerate(headers):
                tk.Label(scrollable_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col_num, padx=5, pady=5)

            # Popula os dados nas colunas
            for i, row in enumerate(rows, start=1):
                for j, value in enumerate(row):
                    tk.Label(scrollable_frame, text=value, font=("Arial", 12)).grid(row=i, column=j, padx=5, pady=2)
        else:
            tk.Label(scrollable_frame, text="Não há registros de inventário.", font=("Arial", 12)).pack(padx=5, pady=5)

        cursor.close()

    except Exception as e:
        print(f"Erro ao abrir nova janela: {e}")
