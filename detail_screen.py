import tkinter as tk
from tkinter import messagebox
from new_window import open_new_window
from inventory_window import open_inventory_window
from historico_roteiros import open_historico_roteiros_window
from inconsistencias_window import open_inconsistencias_window
from dynamics_window import open_dynamics_window
from controle_retencao_window import open_controle_retencao_window  # Importa o script para abrir a janela de controle de retenção
from tkinter import ttk

class DetailApp:
    def __init__(self, root, conn, pedido, nfe):
        self.root = root
        self.conn = conn
        self.pedido = pedido
        self.nfe = nfe
        self.remessa = None  # Remessa será carregada a partir dos dados

        # Cores baseadas na paleta de cores
        bg_color = "#1F3A68"  # Fundo azul-escuro
        fg_color = "#FFFFFF"  # Cor do texto (branco)
        btn_color = "#3B75AF"  # Cor dos botões (azul mais claro)
        btn_hover_color = "#2F598C"  # Cor dos botões ao passar o mouse

        # Estilo da janela principal
        self.root.title(f"Detalhes do Pedido: {pedido} | Nota: {nfe}")
        self.root.geometry("1000x650")
        self.root.configure(bg=bg_color)

        # Configura o grid principal para dividir em colunas
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Frame para os dados básicos (esquerda)
        frame_basic_details = tk.Frame(self.root, bg=bg_color)
        frame_basic_details.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Centralizando os Dados Básicos
        tk.Label(frame_basic_details, text="DADOS BÁSICOS", font=("Arial", 16, "bold"), fg=fg_color, bg=bg_color).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # Labels e valores - Layout em duas colunas
        labels = [
            "Pedido", "Nota", "Filial", "Cidades", "Remessa", "Data Inserção",
            "Chegada na Transportadora", "Data Prev. Entrega", "Status Prazo", "Última Ocorrência",
            "Data Última Ocr.", "Qtd. Volumes", "Valor Nfe", "Subrota"
        ]

        self.values = {}
        for i, label in enumerate(labels):
            row = i + 1
            tk.Label(frame_basic_details, text=label, font=("Arial", 12), fg=fg_color, bg=bg_color, anchor="w").grid(row=row, column=0, sticky="e", padx=5, pady=2)
            value_entry = tk.Entry(frame_basic_details, font=("Arial", 12), state='readonly', disabledbackground=bg_color, disabledforeground=fg_color)
            value_entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
            self.values[label] = value_entry

        # Frame para o histórico de movimentações (direita)
        frame_movements = tk.Frame(self.root, bg=bg_color)
        frame_movements.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        canvas = tk.Canvas(frame_movements, bg=bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_movements, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Carregar os dados do banco e preencher os valores
        self.load_basic_details(pedido, nfe)
        self.load_movements(scrollable_frame, pedido, nfe)

        # Botões fixos na parte inferior
        button_frame = tk.Frame(self.root, bg=bg_color)
        button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)
        button_frame.grid_columnconfigure(4, weight=1)
        button_frame.grid_columnconfigure(5, weight=1)  # Adiciona mais uma coluna para o novo botão

        # Função para alterar a cor ao passar o mouse nos botões
        def on_enter(e, btn):
            btn.config(bg=btn_hover_color)

        def on_leave(e, btn):
            btn.config(bg=btn_color)

        # Criar botões
        self.create_button(button_frame, "HISTÓRICO DE BIPAGENS", self.handle_open_new_window, 0, btn_color, on_enter, on_leave)
        self.create_button(button_frame, "INVENTÁRIO DE FILIAIS", self.handle_open_inventory_window, 1, btn_color, on_enter, on_leave)
        self.create_button(button_frame, "HISTÓRICO DE ROTEIROS", self.handle_open_historico_roteiros_window, 2, btn_color, on_enter, on_leave)
        self.create_button(button_frame, "INCONSISTÊNCIAS", self.handle_open_inconsistencias_window, 3, btn_color, on_enter, on_leave)
        self.create_button(button_frame, "DYNAMICS", self.handle_open_dynamics_window, 4, btn_color, on_enter, on_leave)
        self.create_button(button_frame, "CONTROLE RETENÇÃO", self.handle_open_controle_retencao_window, 5, btn_color, on_enter, on_leave)  # Novo botão

    def create_button(self, parent, text, command, col, btn_color, on_enter, on_leave):
        """Função para criar um botão estilizado"""
        btn = tk.Button(parent, text=text, command=command, width=20, bg=btn_color, fg="white", font=("Arial", 10, "bold"), bd=0)
        btn.grid(row=0, column=col, padx=10, pady=10)
        btn.bind("<Enter>", lambda e: on_enter(e, btn))
        btn.bind("<Leave>", lambda e: on_leave(e, btn))

    def load_basic_details(self, pedido, nfe):
        cursor = self.conn.cursor()
        query = """
        SELECT DISTINCT ON (e.pedido, e."Número Nfe") e.pedido, e."Número Nfe", e.cd, e.cidades, e.remessa, e."Data Inserção", 
               e."Chegada na Transportadora", e."Data Prev. Entrega", e."Status Prazo", e."Última Ocorrência", 
               e."Data Última Ocr.", e."Qtd. Volumes", e."Valor Nfe", d.subrota
        FROM "83_excel" e
        LEFT JOIN "base_d23" d
        ON CAST(e.cep AS BIGINT) BETWEEN CAST(d."CEP INICIAL" AS BIGINT) 
        AND CAST(d."CEP FINAL" AS BIGINT)
        WHERE e.pedido = %s AND e."Número Nfe" = %s
        ORDER BY e.pedido, e."Número Nfe", 
                 CASE 
                     WHEN d.subrota = 'TNG520' THEN 1
                     ELSE 2
                 END;
        """
        cursor.execute(query, (self.pedido, self.nfe))
        row = cursor.fetchone()

        if row:
            labels = [
                "Pedido", "Nota", "Filial", "Cidades", "Remessa", "Data Inserção",
                "Chegada na Transportadora", "Data Prev. Entrega", "Status Prazo", "Última Ocorrência",
                "Data Última Ocr.", "Qtd. Volumes", "Valor Nfe", "Subrota"
            ]
            for i, label in enumerate(labels):
                value = str(row[i])
                if label in ["Pedido", "Remessa", "Qtd. Volumes"]:
                    if value.endswith('.0'):
                        value = value[:-2]
                self.values[label].config(state='normal')
                self.values[label].delete(0, tk.END)
                self.values[label].insert(0, value)
                self.values[label].config(state='readonly')

            # Aqui estamos capturando a remessa
            self.remessa = str(int(float(row[4]))) if row else None
        cursor.close()

    def load_movements(self, scrollable_frame, pedido, nfe):
        cursor = self.conn.cursor()
        query = """
        SELECT m.data_movimentacao::timestamp, m.tipo_da_movimentacao
        FROM "base_movimentacoes" m
        WHERE m.pedido = %s AND m.remessa = (
            SELECT e.remessa
            FROM "83_excel" e
            WHERE e.pedido = %s AND e."Número Nfe" = %s
            LIMIT 1
        )
        ORDER BY m.data_movimentacao::timestamp DESC;
        """
        cursor.execute(query, (self.pedido, self.pedido, self.nfe))
        rows = cursor.fetchall()

        tk.Label(scrollable_frame, text="HISTÓRICO MOVIMENTAÇÕES", font=("Arial", 16, "bold"), fg="white", bg="#1F3A68", anchor="center").grid(row=0, column=0, columnspan=2, pady=(0, 10))

        for i, (data_movimentacao, tipo_da_movimentacao) in enumerate(rows):
            tk.Label(scrollable_frame, text=f"{data_movimentacao} - {tipo_da_movimentacao}", font=("Arial", 12), fg="white", bg="#1F3A68", anchor="w").grid(row=i+1, column=0, sticky="w", padx=5, pady=2)

        cursor.close()

    def handle_open_new_window(self):
        if not self.remessa:
            messagebox.showerror("Erro", "Remessa não encontrada.")
        else:
            open_new_window(self.root, self.conn, self.remessa)

    def handle_open_inventory_window(self):
        if not self.remessa:
            messagebox.showerror("Erro", "Remessa não encontrada.")
        else:
            open_inventory_window(self.root, self.conn, self.remessa)

    def handle_open_historico_roteiros_window(self):
        if not self.remessa:
            messagebox.showerror("Erro", "Remessa não encontrada.")
        else:
            open_historico_roteiros_window(self.root, self.conn, self.pedido, self.remessa)

    def handle_open_inconsistencias_window(self):
        if not self.remessa:
            messagebox.showerror("Erro", "Remessa não encontrada.")
        else:
            open_inconsistencias_window(self.root, self.conn, self.pedido, self.nfe, self.remessa)

    def handle_open_dynamics_window(self):
        if not self.pedido or not self.nfe:
            messagebox.showerror("Erro", "Pedido ou Nota não encontrados.")
        else:
            open_dynamics_window(self.root, self.conn, self.pedido, self.nfe)

    def handle_open_controle_retencao_window(self):
        if not self.pedido or not self.nfe:
            messagebox.showerror("Erro", "Pedido ou Nota não encontrados.")
        else:
            open_controle_retencao_window(self.root, self.conn, self.pedido, self.nfe)  # Chama a função do script controle_retencao_windows
