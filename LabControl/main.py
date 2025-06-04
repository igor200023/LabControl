import tkinter as tk
from models import BancoDeDados, Usuario
from views import LoginScreen

if __name__ == "__main__":
    banco = BancoDeDados()
    usuario = Usuario(banco=banco)
    root = tk.Tk()
    app = LoginScreen(root, usuario=usuario)
    root.mainloop()