import tkinter as tk
import traceback
from db_connection import DatabaseConnectionApp

def main():
    try:
        root = tk.Tk()
        
        # Remova ou comente a linha que define o ícone
        # root.iconbitmap(icon_path)

        app = DatabaseConnectionApp(root)
        root.mainloop()
    except Exception as e:
        # Registrar o erro em um arquivo de log
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())
        # Exibir uma mensagem de erro no console
        print("Ocorreu um erro. Verifique o arquivo error_log.txt para mais detalhes.")

if __name__ == "__main__":
    main()
