import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ctypes  # Necessário para alterar o ícone da barra de tarefas no Windows
import os 
from login_screen import LoginApp
import psycopg2

class DatabaseConnectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conexão ao Banco de Dados")

        # Configuração do ícone da janela e da barra de tarefas
        # self.root.iconbitmap("img/logo-jb.ico")  # Substitua pelo caminho para seu arquivo .ico

        # # Alterar o ícone da barra de tarefas (somente no Windows)
        # if os.name == 'nt':
        #     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
        #     self.root.wm_iconbitmap("img/logo-jb.ico")

        # Configuração para iniciar maximizado
        self.root.state('zoomed')

        # Mudança da cor de fundo
        self.root.configure(bg='#1E1E44')  # Azul escuro

        # Frame para centralizar os campos
        self.center_frame = tk.Frame(root, bg='#1E1E44')
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Adicionar logo acima dos campos de IP e Porta
        self.logo_image = Image.open("img/logo.png")  # Substitua pelo caminho para sua imagem
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.center_frame, image=self.logo, bg='#1E1E44')
        self.logo_label.pack(pady=20)

        # Campo para o IP do banco de dados
        self.ip_label = tk.Label(self.center_frame, text="IP do Banco de Dados:", bg='#1E1E44', fg='white', font=('Arial', 12, 'bold'))
        self.ip_label.pack()
        self.ip_entry = tk.Entry(self.center_frame, font=('Arial', 12), width=30)
        self.ip_entry.insert(0, "192.168.1.160")  # Preenche automaticamente com o valor padrão do IP
        self.ip_entry.pack(pady=10)

        # Campo para a porta do banco de dados com preenchimento automático
        self.port_label = tk.Label(self.center_frame, text="Porta do Banco de Dados:", bg='#1E1E44', fg='white', font=('Arial', 12, 'bold'))
        self.port_label.pack()
        self.port_entry = tk.Entry(self.center_frame, font=('Arial', 12), width=30)
        self.port_entry.insert(0, "5479")  # Preenche automaticamente com 5479
        self.port_entry.pack(pady=10)

        # Botão de conexão com estilização moderna
        self.connect_button = tk.Button(self.center_frame, text="Conectar", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', width=20, height=2, command=self.connect_to_db)
        self.connect_button.pack(pady=20)

        # Adicionar binding para a tecla Enter
        self.root.bind('<Return>', lambda event: self.connect_to_db())

    def connect_to_db(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        try:
            self.conn = psycopg2.connect(
                host=ip,
                port=port,
                user="postgres",
                password="postgres",
                dbname="pedidos"
            )
            messagebox.showinfo("Conexão", "Conexão bem-sucedida!")
            self.root.destroy()
            self.open_login_screen()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar: {str(e)}")

    def open_login_screen(self):
        login_root = tk.Tk()
        LoginApp(login_root, self.conn)
        login_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseConnectionApp(root)
    root.mainloop()
