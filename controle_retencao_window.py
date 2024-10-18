import tkinter as tk
from tkinter import ttk

def open_controle_retencao_window(root, conn, pedido, nfe):
    controle_retencao_window = tk.Toplevel(root)
    controle_retencao_window.title(f"Controle Retenção - Pedido: {pedido}, Nota Fiscal: {nfe}")
    controle_retencao_window.geometry("600x400")

    frame = tk.Frame(controle_retencao_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Label de Título
    tk.Label(frame, text="Controle de Retenção", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(frame, text=f"Exibindo dados de retenção para o Pedido: {pedido} e Nota Fiscal: {nfe}", font=("Arial", 12)).pack(pady=10)

    # Criar a Treeview para mostrar os dados de retenção
    columns = ("ocorrencia", "etapa", "data_criacao", "motivo", "status_retencao")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    tree.heading("ocorrencia", text="Nº da Ocorrência")
    tree.heading("etapa", text="Etapa")
    tree.heading("data_criacao", text="Data da Criação")
    tree.heading("motivo", text="MOTIVO")
    tree.heading("status_retencao", text="Status Retenção")

    tree.column("ocorrencia", anchor=tk.CENTER)
    tree.column("etapa", anchor=tk.CENTER)
    tree.column("data_criacao", anchor=tk.CENTER)
    tree.column("motivo", anchor=tk.CENTER)
    tree.column("status_retencao", anchor=tk.CENTER)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Realizar a consulta no banco de dados para buscar os dados de retenção
    cursor = conn.cursor()
    query = """
    SELECT "Nº DA OCORRÊNCIA", "ETAPA", "DATA DA CRIAÇÃO", "MOTIVO", "STATUS RETENÇÃO"
    FROM base_retencao_pedidos
    WHERE "PEDIDO" = %s AND "NOTA FISCAL" = %s;
    """
    
    # Substituir "pedido" e "nfe" pelos valores adequados
    cursor.execute(query, (pedido, nfe))
    rows = cursor.fetchall()

    # Verificar se há dados e inseri-los na Treeview
    if rows:
        for row in rows:
            tree.insert("", tk.END, values=row)
    else:
        tk.Label(frame, text="Nenhuma retenção encontrada para este pedido e nota fiscal.", font=("Arial", 12)).pack(pady=10)

    cursor.close()

    # Botão para fechar a janela
    close_button = tk.Button(controle_retencao_window, text="Fechar", command=controle_retencao_window.destroy)
    close_button.pack(pady=10)
