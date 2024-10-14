import tkinter as tk

def open_new_window(root, conn, remessa):
    # Criar nova janela com o número da remessa no título
    try:
        new_window = tk.Toplevel(root)
        new_window.title(f"Historico de bipagens - Remessa: {remessa}")

        # Frame para a lista de resultados
        frame_results = tk.Frame(new_window)
        frame_results.pack(padx=10, pady=10)

        cursor = conn.cursor()
        query = """
        SELECT DISTINCT ON ("tipo", "motorista", "Data", "Código de Barras") 
               "tipo", "motorista", "Data", "Código de Barras" 
        FROM base_bipagem 
        WHERE "Código de Barras" LIKE %s
        """
        cursor.execute(query, ('%' + remessa + '%',))
        rows = cursor.fetchall()

        if rows:
            # Cria os cabeçalhos das colunas
            headers = ["Tipo", "Motorista", "Data", "Código de Barras"]
            for col_num, header in enumerate(headers):
                tk.Label(frame_results, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col_num, padx=5, pady=5)

            # Popula os dados nas colunas
            for i, row in enumerate(rows, start=1):
                for j, value in enumerate(row):
                    tk.Label(frame_results, text=value, font=("Arial", 12)).grid(row=i, column=j, padx=5, pady=2)
        else:
            tk.Label(frame_results, text="Não há registros de bipagem.", font=("Arial", 12)).pack(padx=5, pady=5)

        cursor.close()
    except Exception as e:
        print(f"Erro ao abrir nova janela: {e}")
