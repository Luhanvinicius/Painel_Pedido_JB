import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def open_dynamics_window(root, conn, pedido, nfe):
    # Criação da nova janela
    dynamics_window = tk.Toplevel(root)
    dynamics_window.title(f"Dynamics - Pedido: {pedido}, Nota: {nfe}")
    dynamics_window.geometry("600x400")

    # Frame para exibir os resultados
    frame = tk.Frame(dynamics_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Label para título
    tk.Label(frame, text="Dados de Dynamics", font=("Arial", 16, "bold")).pack(pady=(0, 10))

    # Criar o Treeview (tabela)
    columns = ("Data Criação", "NATS", "Etapa", "Data SLA", "Resposta", "Data Resposta")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Definir os cabeçalhos
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True)

    # Realizar a consulta no banco de dados para buscar os dados
    cursor = conn.cursor()
    query = """
    SELECT data_criacao, numero_ocorrencia, etapa, data_sla, solucao, termino_real
    FROM base_nats
    WHERE TRIM(CAST(pedido AS TEXT)) = %s AND TRIM(CAST(numero_nota_fiscal AS TEXT)) = %s;
    """
    cursor.execute(query, (str(pedido).strip(), str(nfe).strip()))  # Garantir que espaços sejam removidos
    result = cursor.fetchone()

    if result:
        # Inserir os dados na tabela
        tree.insert("", "end", values=result)
   
       

    cursor.close()
