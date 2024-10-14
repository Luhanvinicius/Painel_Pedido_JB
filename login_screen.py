import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from table_screen import TableApp

class LoginApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.root.title("Login")

        # Configuração para iniciar maximizado
        self.root.state('zoomed')

        # Mudança da cor de fundo
        self.root.configure(bg='#1E1E44')  # Azul escuro

        # Frame para centralizar os campos
        self.center_frame = tk.Frame(root, bg='#1E1E44')
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Adicionar logo acima dos campos de login
        self.logo_image = Image.open("img/logo.png")  # Substitua pelo caminho para sua imagem
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.center_frame, image=self.logo, bg='#1E1E44')
        self.logo_label.pack(pady=20)

        # Campo para o usuário
        self.user_label = tk.Label(self.center_frame, text="Usuário:", bg='#1E1E44', fg='white', font=('Arial', 12, 'bold'))
        self.user_label.pack()
        self.user_entry = tk.Entry(self.center_frame, font=('Arial', 12), width=30)
        self.user_entry.pack(pady=10)

        # Campo para a senha
        self.password_label = tk.Label(self.center_frame, text="Senha:", bg='#1E1E44', fg='white', font=('Arial', 12, 'bold'))
        self.password_label.pack()
        self.password_entry = tk.Entry(self.center_frame, show="*", font=('Arial', 12), width=30)
        self.password_entry.pack(pady=10)

        # Botão de login com estilização moderna
        self.login_button = tk.Button(self.center_frame, text="Login", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', width=20, height=2, command=self.login)
        self.login_button.pack(pady=20)

        # Vinculando o Enter à função de login
        self.root.bind('<Return>', lambda event: self.login())

    def login(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        
        try:
            cursor = self.conn.cursor()
            query = """
            SELECT * FROM acessos 
            WHERE login = %s AND senha = %s
            """
            cursor.execute(query, (user, password))
            result = cursor.fetchone()
            
            if result:
                messagebox.showinfo("Login", "Login realizado com sucesso!")
                self.root.destroy()
                self.open_table_screen()
            else:
                messagebox.showerror("Erro", "Login ou senha incorretos.")
            
            cursor.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao realizar login: {str(e)}")

    def open_table_screen(self):
        table_root = tk.Tk()
        TableApp(table_root, self.conn)
        table_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    conn = None  # Substitua com a conexão ao banco de dados real
    app = LoginApp(root, conn)
    root.mainloop()
