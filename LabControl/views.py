import tkinter as tk
from tkinter import ttk, messagebox
from config import *
from models import Usuario
import sqlite3

class LoginScreen:
    def __init__(self, root, usuario: Usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("LabControl - Login")
        self.root.geometry("800x500")
        self.root.configure(bg=COR_FUNDO)
        
        self.centralizar_janela()
        self.criar_widgets()

    def centralizar_janela(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def criar_widgets(self):
        self.main_frame = tk.Frame(
            self.root, 
            bg="white", 
            bd=0, 
            highlightthickness=1,
            highlightbackground="#ddd",
            highlightcolor="#ddd",
            relief=tk.RAISED
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=500)
        
        left_frame = tk.Frame(self.main_frame, bg=COR_PRIMARIA)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        logo_label = tk.Label(
            left_frame,
            text="🔬 LabControl",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg=COR_PRIMARIA
        )
        logo_label.pack(pady=150)
        
        slogan_label = tk.Label(
            left_frame,
            text="Sistema de Gerenciamento de Laboratório",
            font=("Segoe UI", 12),
            fg="#e0e0e0",
            bg=COR_PRIMARIA
        )
        slogan_label.pack()
        
        right_frame = tk.Frame(self.main_frame, bg="white", padx=40, pady=50)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            right_frame,
            text="Acessar Sistema",
            font=("Segoe UI", 20, "bold"),
            fg=COR_TEXTO,
            bg="white"
        )
        title_label.pack(pady=(0, 30))
        
        user_frame = tk.Frame(right_frame, bg="white")
        user_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            user_frame,
            text="Usuário",
            font=FONTE_PADRAO,
            bg="white",
            fg="#666"
        ).pack(anchor='w')
        
        self.user_entry = ttk.Entry(user_frame, font=FONTE_PADRAO)
        self.user_entry.pack(fill=tk.X, pady=(5, 0))
        
        pass_frame = tk.Frame(right_frame, bg="white")
        pass_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(
            pass_frame,
            text="Senha",
            font=FONTE_PADRAO,
            bg="white",
            fg="#666"
        ).pack(anchor='w')
        
        self.pass_entry = ttk.Entry(pass_frame, font=FONTE_PADRAO, show="*")
        self.pass_entry.pack(fill=tk.X, pady=(5, 0))
        
        login_btn = ttk.Button(right_frame, text="ENTRAR", command=self.login)
        login_btn.pack(fill=tk.X, pady=(0, 20))
        
        register_link = tk.Label(
            right_frame,
            text="Não tem uma conta? Cadastre-se",
            font=("Segoe UI", 9),
            fg=COR_PRIMARIA,
            bg="white",
            cursor="hand2"
        )
        register_link.pack()
        register_link.bind("<Button-1>", lambda e: self.ir_para_cadastro())
        
        self.root.bind('<Return>', lambda event: self.login())
        self.user_entry.focus()

    def login(self):
        usuario = self.user_entry.get()
        senha = self.pass_entry.get()
        
        if self.usuario.verificar_login(usuario, senha):
            self.root.destroy()
            from controllers import LabControlApp
            root_principal = tk.Tk()
            app = LabControlApp(root_principal, banco=self.usuario.banco, usuario_atual=usuario)
            root_principal.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    def ir_para_cadastro(self):
        self.root.destroy()
        root_cadastro = tk.Tk()
        app_cadastro = CadastroScreen(root_cadastro, usuario=self.usuario)
        root_cadastro.mainloop()

class CadastroScreen:
    def __init__(self, root, usuario: Usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("LabControl - Cadastro")
        self.root.geometry("600x400")
        self.root.configure(bg=COR_FUNDO)
        
        self.centralizar_janela()
        self.criar_widgets()

    def centralizar_janela(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def criar_widgets(self):
        self.main_frame = tk.Frame(
            self.root, 
            bg="white", 
            bd=0, 
            highlightthickness=1,
            highlightbackground="#ddd",
            highlightcolor="#ddd",
            relief=tk.RAISED
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)
        
        title_label = tk.Label(
            self.main_frame,
            text="Criar Nova Conta",
            font=("Segoe UI", 20, "bold"),
            fg=COR_TEXTO,
            bg="white"
        )
        title_label.pack(pady=(40, 30))
        
        form_frame = tk.Frame(self.main_frame, bg="white", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        user_frame = tk.Frame(form_frame, bg="white")
        user_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            user_frame,
            text="Nome de Usuário",
            font=FONTE_PADRAO,
            bg="white",
            fg="#666"
        ).pack(anchor='w')
        
        self.user_entry = ttk.Entry(user_frame, font=FONTE_PADRAO)
        self.user_entry.pack(fill=tk.X, pady=(5, 0))
        
        pass_frame = tk.Frame(form_frame, bg="white")
        pass_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            pass_frame,
            text="Senha",
            font=FONTE_PADRAO,
            bg="white",
            fg="#666"
        ).pack(anchor='w')
        
        self.pass_entry = ttk.Entry(pass_frame, font=FONTE_PADRAO, show="*")
        self.pass_entry.pack(fill=tk.X, pady=(5, 0))
        
        confirm_frame = tk.Frame(form_frame, bg="white")
        confirm_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(
            confirm_frame,
            text="Confirmar Senha",
            font=FONTE_PADRAO,
            bg="white",
            fg="#666"
        ).pack(anchor='w')
        
        self.confirm_entry = ttk.Entry(confirm_frame, font=FONTE_PADRAO, show="*")
        self.confirm_entry.pack(fill=tk.X, pady=(5, 0))
        
        register_btn = ttk.Button(form_frame, text="CADASTRAR", command=self.cadastrar)
        register_btn.pack(fill=tk.X, pady=(0, 20))
        
        login_link = tk.Label(
            form_frame,
            text="← Voltar para o login",
            font=("Segoe UI", 9),
            fg=COR_PRIMARIA,
            bg="white",
            cursor="hand2"
        )
        login_link.pack()
        login_link.bind("<Button-1>", lambda e: self.abrir_tela_login())
        
        self.root.bind('<Return>', lambda event: self.cadastrar())
        self.user_entry.focus()

    def cadastrar(self):
        usuario = self.user_entry.get().strip()
        senha = self.pass_entry.get().strip()
        confirmacao = self.confirm_entry.get().strip()
        
        if not usuario or not senha or not confirmacao:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")
            return
            
        if len(usuario) < 4:
            messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 4 caracteres")
            return
            
        if len(senha) < 6:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 6 caracteres")
            return
            
        if senha != confirmacao:
            messagebox.showerror("Erro", "As senhas não coincidem")
            return
            
        try:
            self.usuario.criar_usuario(usuario, senha)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.abrir_tela_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este nome de usuário já está em uso")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def abrir_tela_login(self):
        self.root.destroy()
        root_login = tk.Tk()
        from views import LoginScreen
        app_login = LoginScreen(root_login, usuario=self.usuario)
        root_login.mainloop()