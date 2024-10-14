import tkinter as tk
from tkinter import messagebox

def open_inconsistencias_window(root, conn, pedido, nfe):
    # Criação da nova janela
    inconsistencias_window = tk.Toplevel(root)
    inconsistencias_window.title(f"Inconsistências - Pedido: {pedido}, Nota: {nfe}")
    inconsistencias_window.geometry("400x600")

    # Frame para exibir os resultados
    frame = tk.Frame(inconsistencias_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Label para título
    tk.Label(frame, text="Notificação de Inconsistências", font=("Arial", 16, "bold")).pack(pady=(0, 10))

    # Realizar a consulta no banco de dados para buscar a notificação, caixa_faltante e data_envio
    cursor = conn.cursor()
    query = """
    SELECT data_envio, notificacao, retorno_ocorrencia, problema, situacao, acao, apontamento
    FROM base_controle
    WHERE pedido = %s AND "nf" = %s;
    """
    cursor.execute(query, (pedido, nfe))
    result = cursor.fetchone()

    if result:
        # Desempacotar os resultados
        data_envio = result[0]
        notificacao = result[1]
        retorno_ocorrencia = result[2]
        problema = result[3]
        situacao = result[4]
        acao = result[5]
        apontamento = result[6]

        # Exibir os resultados em labels
        tk.Label(frame, text=f"DATA NOTIFICAÇÃO: {data_envio}", font=("Arial", 12), wraplength=350).pack(pady=10)
        tk.Label(frame, text=f"TIPO NOTIFICAÇÃO: {notificacao}", font=("Arial", 12), wraplength=350).pack(pady=10)
        tk.Label(frame, text=f"DATA RESPOSTA NATURA: {retorno_ocorrencia}", font=("Arial", 12), wraplength=350).pack(pady=10)
        tk.Label(frame, text=f"PROBLEMA NATURA: {problema}", font=("Arial", 12), wraplength=350).pack(pady=10)
        tk.Label(frame, text=f"SITUAÇÃO NATURA: {situacao}", font=("Arial", 12), wraplength=350).pack(pady=10)
        tk.Label(frame, text=f"AÇÃO JB: {acao}", font=("Arial", 12), wraplength=350).pack(pady=10)
        tk.Label(frame, text=f"APONTAMENTO JB: {apontamento}", font=("Arial", 12), wraplength=350).pack(pady=10)
        
    else:
        tk.Label(frame, text="Nenhuma inconsistência encontrada.", font=("Arial", 12), wraplength=350).pack(pady=10)

    cursor.close()
