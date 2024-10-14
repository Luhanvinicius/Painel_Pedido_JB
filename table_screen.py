import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from detail_screen import DetailApp

class TableApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("Tabela de Dados")
        self.root.state('zoomed')
        self.root.configure(bg='#1E1E44')  # Azul escuro
        self.detail_window_open = False  # Controle para a janela de detalhes

        # Frame principal que conterá a logo e os campos de entrada
        self.main_frame = tk.Frame(root, bg='#1E1E44')
        self.main_frame.pack(pady=20)

        # Frame para a logo
        self.logo_frame = tk.Frame(self.main_frame, bg='#1E1E44')
        self.logo_frame.pack(side='left', padx=20)

        # Adicionar logo à esquerda dos campos de entrada
        self.logo_image = Image.open("img/logo.png")  # Substitua pelo caminho para sua imagem
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.logo_frame, image=self.logo, bg='#1E1E44')
        self.logo_label.pack()

        # Frame para os campos de entrada, à direita da logo
        self.entry_frame = tk.Frame(self.main_frame, bg='#1E1E44')
        self.entry_frame.pack(side='left', padx=20)

        # Campos de entrada para Pedido, Remessa e Número Nfe
        self.pedido_label = tk.Label(self.entry_frame, text="Pedido:", bg='#1E1E44', fg='white', font=('Arial', 12, 'bold'))
        self.pedido_label.pack()
        self.pedido_entry = tk.Entry(self.entry_frame, font=('Arial', 12), width=30)
        self.pedido_entry.pack(pady=5)

        self.remessa_label = tk.Label(self.entry_frame, text="Remessa:", bg='#1E1E44', fg='white', font=('Arial', 12, 'bold'))
        self.remessa_label.pack()
        self.remessa_entry = tk.Entry(self.entry_frame, font=('Arial', 12), width=30)
        self.remessa_entry.pack(pady=5)

        self.nfe_label = tk.Label(self.entry_frame, text="Número Nfe:", bg='#1E1E44', fg='white', font=('Arial', 12, 'bold'))
        self.nfe_label.pack()
        self.nfe_entry = tk.Entry(self.entry_frame, font=('Arial', 12), width=30)
        self.nfe_entry.pack(pady=5)

        # Botão de Pesquisa com estilização moderna
        self.search_button = tk.Button(self.entry_frame, text="Pesquisar", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', width=20, height=2, command=self.search_data)
        self.search_button.pack(pady=10)

        # Vincular o evento "Enter" ao botão de pesquisa
        self.root.bind('<Return>', lambda event: self.search_button.invoke())

        # Configuração da Treeview
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(fill='both', expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("cd", "pedido", "Número Nfe", "Data Inserção", "Cidades", "Remessa", "Data Prev. Entrega", "Qtd. Volumes", "Última Ocorrência"), show='headings')
        self.tree.pack(fill='both', expand=True)

        # Definir colunas
        self.tree.heading("cd", text="Filial")
        self.tree.heading("pedido", text="Pedido")
        self.tree.heading("Número Nfe", text="Número Nfe")
        self.tree.heading("Data Inserção", text="Data Inserção")
        self.tree.heading("Cidades", text="Cidades")
        self.tree.heading("Remessa", text="Remessa")
        self.tree.heading("Data Prev. Entrega", text="Data Prev. Entrega")
        self.tree.heading("Qtd. Volumes", text="Qtd. Volumes")
        self.tree.heading("Última Ocorrência", text="Última Ocorrência")

        # Configuração das colunas
        for col in self.tree["columns"]:
            self.tree.column(col, anchor=tk.CENTER)

        # Evento de duplo clique
        self.tree.bind("<Double-1>", self.on_item_double_click)

    def search_data(self):
        pedido = self.pedido_entry.get().strip()
        remessa = self.remessa_entry.get().strip()
        nfe = self.nfe_entry.get().strip()

        # Verificar se pelo menos um campo foi preenchido
        if not pedido and not remessa and not nfe:
            messagebox.showerror("Erro", "Por favor, preencha pelo menos um campo para a busca.")
            return

        # Limpar a Treeview antes de exibir os novos resultados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Construir a consulta SQL dinamicamente com base nos critérios fornecidos
        query = """
        SELECT "cd", "pedido", "Número Nfe", "Data Inserção", cidades, remessa, "Data Prev. Entrega", "Qtd. Volumes", "Última Ocorrência"
        FROM "83_excel"
        WHERE 1=1
        """
        params = []

        if pedido:
            query += " AND pedido = %s"
            params.append(pedido)
        if remessa:
            query += " AND remessa = %s"
            params.append(remessa)
        if nfe:
            query += " AND \"Número Nfe\" = %s"
            params.append(nfe)

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            if pedido:
                messagebox.showinfo("Pedido não encontrado", f"Pedido '{pedido}' não foi encontrado.")
            if remessa:
                messagebox.showinfo("Remessa não encontrada", f"Remessa '{remessa}' não foi encontrada.")
            if nfe:
                messagebox.showinfo("Número Nfe não encontrado", f"Número Nfe '{nfe}' não foi encontrado.")
            return

        for row in rows:
            # Convert values to strings and remove .0 if present
            row = tuple(
                str(value)[:-2] if isinstance(value, float) and value.is_integer() else str(value)
                for value in row
            )
            self.tree.insert("", tk.END, values=row)

        cursor.close()

    def on_item_double_click(self, event):
        if not self.detail_window_open:  # Verificar se a janela de detalhes já está aberta
            self.detail_window_open = True

            # Obter o item selecionado
            selected_item = self.tree.selection()[0]
            item_values = self.tree.item(selected_item, 'values')

            # Extrair informações do item selecionado
            pedido = item_values[1]
            nfe = item_values[2]

            # Abrir nova tela com detalhes
            self.open_detail_screen(pedido, nfe)

    def open_detail_screen(self, pedido, nfe):
        detail_root = tk.Tk()

        # Ao fechar a janela de detalhes, permitir novamente a abertura de novas janelas
        def on_close():
            self.detail_window_open = False
            detail_root.destroy()

        detail_root.protocol("WM_DELETE_WINDOW", on_close)
        DetailApp(detail_root, self.conn, pedido, nfe)
        detail_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    conn = None  # Substitua pela conexão real com o banco de dados
    app = TableApp(root, conn)
    root.mainloop()
