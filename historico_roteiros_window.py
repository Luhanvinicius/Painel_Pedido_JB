import tkinter as tk
from tkinter import ttk

def open_historico_roteiros_window(root, conn, pedido, remessa):
    try:
        new_window = tk.Toplevel(root)
        new_window.title(f"Histórico de Roteiros - Pedido: {pedido}, Remessa: {remessa}")

        container = tk.Frame(new_window)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        cursor = conn.cursor()
        query = """
        SELECT "data_de_emissão", "roteiro", "motorista", "status", "motivo", "data"
        FROM base_entregas
        WHERE "pedido" = %s AND "remessa" = %s
        """
        cursor.execute(query, (pedido, remessa))
        rows = cursor.fetchall()

        if rows:
            headers = ["Data de Emissão", "Roteiro", "Motorista", "Status", "Motivo", "Data"]
            for col_num, header in enumerate(headers):
                tk.Label(scrollable_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col_num, padx=5, pady=5)

            for i, row in enumerate(rows, start=1):
                for j, value in enumerate(row):
                    tk.Label(scrollable_frame, text=value, font=("Arial", 12)).grid(row=i, column=j, padx=5, pady=2)
        else:
            tk.Label(scrollable_frame, text="Não há registros de roteiros.", font=("Arial", 12)).pack(padx=5, pady=5)

        cursor.close()

    except Exception as e:
        print(f"Erro ao abrir nova janela: {e}")
