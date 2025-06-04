import tkinter as tk
from tkinter import ttk, messagebox, font
import datetime
from config import *
from models import BancoDeDados
import sqlite3
from models import Usuario

class LabControlApp:
    def __init__(self, root, banco: BancoDeDados, usuario_atual):
        self.root = root
        self.banco = banco
        self.usuario_atual = usuario_atual
        self.root.title("Labcontrol")
        self.root.geometry("900x600")
        self.root.configure(bg=COR_FUNDO)
        
        self.configurar_estilos()
        self.criar_widgets()

    def configurar_estilos(self):
        """Configura os estilos padrão para widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
            background=COR_FUNDO,
            foreground=COR_TEXTO,
            rowheight=25,
            fieldbackground=COR_FUNDO,
            font=FONTE_PADRAO,
            bordercolor="#ddd",
            borderwidth=1
        )
        style.configure("Treeview.Heading",
            font=FONTE_BOTOES,
            background=COR_PRIMARIA,
            foreground="white",
            relief="flat"
        )
        style.map("Treeview.Heading",
            background=[('active', COR_SECUNDARIA)]
        )
        
        style.configure("TButton",
            font=FONTE_BOTOES,
            padding=6,
            relief="flat",
            background=COR_PRIMARIA,
            foreground="white"
        )
        style.map("TButton",
            background=[('active', COR_SECUNDARIA), ('disabled', '#ccc')]
        )
        
        style.configure("TEntry",
            fieldbackground="white",
            foreground=COR_TEXTO,
            bordercolor="#ddd",
            lightcolor="#ddd",
            darkcolor="#ddd",
            padding=5,
            insertcolor=COR_PRIMARIA,
            font=FONTE_PADRAO
        )

    def criar_widgets(self):
        """Cria todos os widgets da interface principal"""
        
        self.main_container = tk.Frame(self.root, bg=COR_FUNDO)
        self.main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        self.header_frame = tk.Frame(self.main_container, bg=COR_PRIMARIA, height=120)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_frame = tk.Frame(self.header_frame, bg=COR_PRIMARIA)
        self.title_frame.pack(side=tk.LEFT, padx=30, pady=20)
        
        self.title_label = tk.Label(
            self.title_frame,
            text="LABCONTROL",
            font=FONTE_TITULO,
            fg="white",
            bg=COR_PRIMARIA
        )
        self.title_label.pack(anchor='w')
        
        self.subtitle_label = tk.Label(
            self.title_frame,
            text="Sistema de Gerenciamento de Laboratório",
            font=FONTE_SUBTITULO,
            fg="#e0e0e0",
            bg=COR_PRIMARIA
        )
        self.subtitle_label.pack(anchor='w')
        
        
        self.info_frame = tk.Frame(self.header_frame, bg=COR_PRIMARIA)
        self.info_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
        self.data_label = tk.Label(
            self.info_frame,
            text=f"📅 {data_atual}",
            font=FONTE_PADRAO,
            fg="white",
            bg=COR_PRIMARIA
        )
        self.data_label.pack(anchor='e')
        
        self.user_label = tk.Label(
            self.info_frame,
            text=f"👤 {self.usuario_atual}",
            font=FONTE_PADRAO,
            fg="white",
            bg=COR_PRIMARIA
        )
        self.user_label.pack(anchor='e')
        
        
        self.cards_frame = tk.Frame(self.main_container, bg=COR_FUNDO)
        self.cards_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        self.criar_card("Registrar Empréstimo", "📝", "Registre novos empréstimos de equipamentos", self.registrar_emprestimo, 0)
        self.criar_card("Empréstimos Ativos", "📋", "Visualize empréstimos em andamento", self.exibir_emprestimos, 1)
        self.criar_card("Histórico", "🕒", "Consulte o histórico de devoluções", self.exibir_historico, 2)
        
        
        self.footer_frame = tk.Frame(self.main_container, bg=COR_FUNDO)
        self.footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        
        self.modo_btn = tk.Button(
            self.footer_frame,
            text="🌙 Modo Escuro" if not modo_escuro_ativo else "☀️ Modo Claro",
            font=FONTE_PADRAO,
            bg=COR_TERCIARIA if not modo_escuro_ativo else COR_PRIMARIA,
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            command=self.toggle_modo_escuro
        )
        self.modo_btn.pack(side=tk.LEFT, padx=10)
        
        
        self.logout_btn = tk.Button(
            self.footer_frame,
            text="🚪 Sair",
            font=FONTE_PADRAO,
            bg=COR_ERRO,
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            command=self.logout
        )
        self.logout_btn.pack(side=tk.RIGHT, padx=10)
        
        
        if self.usuario_atual == "admin":
            self.users_btn = tk.Button(
                self.footer_frame,
                text="👥 Gerenciar Usuários",
                font=FONTE_PADRAO,
                bg=COR_SUCESSO,
                fg="white",
                bd=0,
                padx=15,
                pady=5,
                command=self.gerenciar_usuarios
            )
            self.users_btn.pack(side=tk.RIGHT, padx=10)
        
        
        self.configurar_hover_effects()

    def criar_card(self, titulo, icone, descricao, comando, posicao):
        """Cria um card estilizado para cada funcionalidade"""
        card = tk.Frame(
            self.cards_frame,
            bg="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#ddd",
            highlightcolor="#ddd",
            relief=tk.RAISED
        )
        
        
        if posicao % 3 == 0:
            card.grid(row=posicao//3, column=0, padx=10, pady=10, sticky="nsew")
        elif posicao % 3 == 1:
            card.grid(row=posicao//3, column=1, padx=10, pady=10, sticky="nsew")
        else:
            card.grid(row=posicao//3, column=2, padx=10, pady=10, sticky="nsew")
        
        
        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(1, weight=1)
        self.cards_frame.grid_columnconfigure(2, weight=1)
        self.cards_frame.grid_rowconfigure(posicao//3, weight=1)
        
        
        icon_label = tk.Label(
            card,
            text=icone,
            font=("Segoe UI", 24),
            bg="white",
            fg=COR_PRIMARIA
        )
        icon_label.pack(pady=(20, 10))
        
        title_label = tk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=COR_TEXTO
        )
        title_label.pack(pady=(0, 5))
        
        desc_label = tk.Label(
            card,
            text=descricao,
            font=FONTE_PADRAO,
            bg="white",
            fg="#666",
            wraplength=200
        )
        desc_label.pack(pady=(0, 20), padx=20)
        
        action_btn = tk.Button(
            card,
            text="Acessar",
            font=FONTE_BOTOES,
            bg=COR_PRIMARIA,
            fg="white",
            activebackground=COR_SECUNDARIA,
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5,
            command=comando
        )
        action_btn.pack(pady=(0, 20))
        
        
        card.bind("<Enter>", lambda e, c=card: c.config(highlightbackground=COR_PRIMARIA, highlightcolor=COR_PRIMARIA))
        card.bind("<Leave>", lambda e, c=card: c.config(highlightbackground="#ddd", highlightcolor="#ddd"))
        
        return card

    def configurar_hover_effects(self):
        """Configura efeitos hover para botões"""
        buttons = [self.modo_btn, self.logout_btn]
        if self.usuario_atual == "admin":
            buttons.append(self.users_btn)
        
        for btn in buttons:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COR_SECUNDARIA if b != self.logout_btn else "#c0392b"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(
                bg=COR_TERCIARIA if b == self.modo_btn and not modo_escuro_ativo else 
                COR_PRIMARIA if b == self.modo_btn and modo_escuro_ativo else
                COR_SUCESSO if b == self.users_btn else COR_ERRO
            ))

    def toggle_modo_escuro(self):
        """Alterna entre modo claro e escuro"""
        global modo_escuro_ativo
        modo_escuro_ativo = not modo_escuro_ativo
        
        if modo_escuro_ativo:
            self.aplicar_modo_escuro()
        else:
            self.aplicar_modo_claro()

    def aplicar_modo_escuro(self):
        """Aplica o tema escuro a todos os elementos"""
        
        self.root.configure(bg=COR_FUNDO_ESCURO)
        self.main_container.configure(bg=COR_FUNDO_ESCURO)
        self.cards_frame.configure(bg=COR_FUNDO_ESCURO)
        self.footer_frame.configure(bg=COR_FUNDO_ESCURO)
        
        
        self.modo_btn.config(text="☀️ Modo Claro", bg=COR_PRIMARIA)
        
        
        for widget in self.cards_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=COR_CARD_ESCURO, highlightbackground=COR_PRIMARIA)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=COR_CARD_ESCURO, fg=COR_TEXTO_ESCURO)
                    elif isinstance(child, tk.Button):
                        child.configure(bg=COR_PRIMARIA, activebackground=COR_SECUNDARIA)
        
        
        self.configurar_hover_effects()

    def aplicar_modo_claro(self):
        """Aplica o tema claro a todos os elementos"""
        
        self.root.configure(bg=COR_FUNDO)
        self.main_container.configure(bg=COR_FUNDO)
        self.cards_frame.configure(bg=COR_FUNDO)
        self.footer_frame.configure(bg=COR_FUNDO)
        
        
        self.modo_btn.config(text="🌙 Modo Escuro", bg=COR_TERCIARIA)
        
        
        for widget in self.cards_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg="white", highlightbackground="#ddd")
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg="white", fg=COR_TEXTO)
                    elif isinstance(child, tk.Button):
                        child.configure(bg=COR_PRIMARIA, activebackground=COR_SECUNDARIA)
        
        
        self.configurar_hover_effects()

    def logout(self):
        """Encerra a sessão e volta para a tela de login"""
        self.root.destroy()
        root_login = tk.Tk()
        from views import LoginScreen
        app_login = LoginScreen(root_login, usuario=Usuario(self.banco))
        root_login.mainloop()

    def registrar_emprestimo(self):
        """Abre janela para registrar novo empréstimo"""
        janela = tk.Toplevel(self.root)
        janela.title("Registrar Empréstimo")
        janela.geometry("600x600")
        janela.resizable(False, False)
        janela.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO, 
                            padx=20, pady=20, bd=0, highlightthickness=1,
                            highlightbackground="#ddd" if not modo_escuro_ativo else COR_PRIMARIA)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="📝 Registrar Empréstimo",
            font=("Segoe UI", 16, "bold"),
            bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
            fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
        )
        title_label.pack(pady=(0, 20))
        
        
        campos = ["Nome Completo", "CPF", "Turma", "Data (dd/mm/aaaa)", "Item Emprestado"]
        entradas = []
        
        for campo in campos:
            
            field_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
            field_frame.pack(fill=tk.X, pady=5)
            
            
            tk.Label(
                field_frame,
                text=campo,
                font=FONTE_PADRAO,
                bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
                fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
            ).pack(anchor='w', padx=(0, 10))
            
            
            entry = ttk.Entry(
                field_frame,
                font=FONTE_PADRAO,
                width=30
            )
            entry.pack(fill=tk.X, pady=2)
            entradas.append(entry)
        
        
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
        entradas[3].insert(0, data_atual)
        
        
        btn_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
        btn_frame.pack(pady=(20, 0))
        
        
        save_btn = ttk.Button(
            btn_frame,
            text="Salvar Empréstimo",
            command=lambda: self.salvar_emprestimo(entradas, janela)
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancelar",
            command=janela.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        
        style = ttk.Style()
        style.configure("TButton", font=FONTE_BOTOES)
        style.map("TButton",
            background=[('active', COR_SECUNDARIA)],
            foreground=[('active', 'white')]
        )

    def salvar_emprestimo(self, entradas, janela):
        """Salva um novo empréstimo no banco de dados"""
        dados = [e.get() for e in entradas]
        
        
        if not all(dados):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!", parent=janela)
            return
            
        
        try:
            dia, mes, ano = map(int, dados[3].split('/'))
            datetime.datetime(ano, mes, dia)
        except:
            messagebox.showerror("Erro", "Data inválida! Use o formato dd/mm/aaaa", parent=janela)
            return
        
        
        self.banco.inserir_emprestimo(*dados)
        messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!", parent=janela)
        janela.destroy()

    def exibir_emprestimos(self):
        """Exibe todos os empréstimos em andamento"""
        janela = tk.Toplevel(self.root)
        janela.title("Empréstimos em Andamento")
        janela.geometry("900x600")
        janela.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="📋 Empréstimos em Andamento",
            font=("Segoe UI", 16, "bold"),
            bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO,
            fg=COR_TEXTO_ESCURO if modo_escuro_ativo else COR_TEXTO
        )
        title_label.pack(anchor='w', pady=(0, 10))
        
        
        tree_frame = tk.Frame(main_frame, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        tree_frame.pack(expand=True, fill=tk.BOTH)
        
        
        y_scroll = ttk.Scrollbar(tree_frame)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("id", "nome", "cpf", "turma", "data", "item"),
            show='headings',
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        tree.pack(expand=True, fill=tk.BOTH)
        
        
        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)
        
        
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("cpf", text="CPF")
        tree.heading("turma", text="Turma")
        tree.heading("data", text="Data")
        tree.heading("item", text="Item")
        
        
        tree.column("id", width=50, anchor='center')
        tree.column("nome", width=200)
        tree.column("cpf", width=120, anchor='center')
        tree.column("turma", width=100, anchor='center')
        tree.column("data", width=100, anchor='center')
        tree.column("item", width=200)
        
        
        for row in self.banco.obter_emprestimos():
            tree.insert('', tk.END, values=row)
        
        
        btn_frame = tk.Frame(main_frame, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        
        ttk.Button(
            btn_frame,
            text="Editar",
            command=lambda: self.editar_emprestimo_selecionado(tree, janela)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Deletar",
            command=lambda: self.deletar_emprestimo_selecionado(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Dar Baixa",
            command=lambda: self.dar_baixa_emprestimo(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Atualizar",
            command=lambda: self.atualizar_lista_emprestimos(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Fechar",
            command=janela.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def editar_emprestimo_selecionado(self, tree, parent):
        """Abre janela para editar empréstimo selecionado"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para editar", parent=parent)
            return
            
        dados = tree.item(selecionado)['values']
        
        janela_edicao = tk.Toplevel(parent)
        janela_edicao.title("Editar Empréstimo")
        janela_edicao.geometry("600x600")
        janela_edicao.resizable(False, False)
        janela_edicao.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela_edicao, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO, 
                            padx=20, pady=20, bd=0, highlightthickness=1,
                            highlightbackground="#ddd" if not modo_escuro_ativo else COR_PRIMARIA)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="✏️ Editar Empréstimo",
            font=("Segoe UI", 16, "bold"),
            bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
            fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
        )
        title_label.pack(pady=(0, 20))
        
        
        campos = ["Nome Completo", "CPF", "Turma", "Data (dd/mm/aaaa)", "Item Emprestado"]
        entradas = []
        
        for i, campo in enumerate(campos):
            
            field_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
            field_frame.pack(fill=tk.X, pady=5)
            
            
            tk.Label(
                field_frame,
                text=campo,
                font=FONTE_PADRAO,
                bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
                fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
            ).pack(anchor='w', padx=(0, 10))
            
            
            entry = ttk.Entry(
                field_frame,
                font=FONTE_PADRAO,
                width=30
            )
            entry.insert(0, dados[i+1])  
            entry.pack(fill=tk.X, pady=2)
            entradas.append(entry)
        
        
        btn_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
        btn_frame.pack(pady=(20, 0))
        
        
        save_btn = ttk.Button(
            btn_frame,
            text="Salvar Alterações",
            command=lambda: self.salvar_edicao_emprestimo(dados[0], entradas, tree, janela_edicao, parent)
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancelar",
            command=janela_edicao.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def salvar_edicao_emprestimo(self, id_, entradas, tree, janela_edicao, parent):
        """Salva as alterações de um empréstimo editado"""
        novos_dados = [e.get() for e in entradas]
        
        
        if not all(novos_dados):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!", parent=janela_edicao)
            return
            
        
        try:
            dia, mes, ano = map(int, novos_dados[3].split('/'))
            datetime.datetime(ano, mes, dia)
        except:
            messagebox.showerror("Erro", "Data inválida! Use o formato dd/mm/aaaa", parent=janela_edicao)
            return
        
        
        self.banco.atualizar_emprestimo(id_, *novos_dados)
        messagebox.showinfo("Sucesso", "Empréstimo atualizado com sucesso!", parent=janela_edicao)
        
        
        self.atualizar_lista_emprestimos(tree)
        
        
        janela_edicao.destroy()
        parent.destroy()
        self.exibir_emprestimos()

    def deletar_emprestimo_selecionado(self, tree):
        """Deleta o empréstimo selecionado"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para deletar")
            return
            
        confirmacao = messagebox.askyesno(
            "Confirmar Exclusão",
            "Tem certeza que deseja deletar este empréstimo?",
            icon='warning'
        )
        
        if confirmacao:
            id_ = tree.item(selecionado)['values'][0]
            self.banco.deletar_emprestimo(id_)
            tree.delete(selecionado)
            messagebox.showinfo("Sucesso", "Empréstimo deletado com sucesso!")

    def dar_baixa_emprestimo(self, tree):
        """Registra a baixa de um empréstimo selecionado"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para dar baixa")
            return
            
        dados = tree.item(selecionado)['values']
        confirmacao = messagebox.askyesno(
            "Confirmar Baixa",
            f"Confirmar baixa do empréstimo para {dados[1]}?",
            icon='question'
        )
        
        if confirmacao:
            self.banco.dar_baixa(*dados[:6]) 
            tree.delete(selecionado)
            messagebox.showinfo("Sucesso", "Baixa registrada com sucesso!")

    def atualizar_lista_emprestimos(self, tree):
        """Atualiza a lista de empréstimos exibida"""
        for item in tree.get_children():
            tree.delete(item)
            
        for row in self.banco.obter_emprestimos():
            tree.insert('', tk.END, values=row)

    def exibir_historico(self):
        """Exibe o histórico de empréstimos devolvidos"""
        janela = tk.Toplevel(self.root)
        janela.title("Histórico de Devoluções")
        janela.geometry("1000x700")
        janela.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="🕒 Histórico de Devoluções",
            font=("Segoe UI", 16, "bold"),
            bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO,
            fg=COR_TEXTO_ESCURO if modo_escuro_ativo else COR_TEXTO
        )
        title_label.pack(anchor='w', pady=(0, 10))
        
        
        tree_frame = tk.Frame(main_frame, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        tree_frame.pack(expand=True, fill=tk.BOTH)
        
        
        y_scroll = ttk.Scrollbar(tree_frame)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("id", "nome", "cpf", "turma", "data", "item"),
            show='headings',
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )
        tree.pack(expand=True, fill=tk.BOTH)
        
        
        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)
        
        
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("cpf", text="CPF")
        tree.heading("turma", text="Turma")
        tree.heading("data", text="Data")
        tree.heading("item", text="Item")
        
        
        tree.column("id", width=50, anchor='center')
        tree.column("nome", width=200)
        tree.column("cpf", width=120, anchor='center')
        tree.column("turma", width=100, anchor='center')
        tree.column("data", width=100, anchor='center')
        tree.column("item", width=200)
        
        
        for row in self.banco.obter_historico():
            tree.insert('', tk.END, values=row)
        
        
        btn_frame = tk.Frame(main_frame, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        
        ttk.Button(
            btn_frame,
            text="Deletar Selecionados",
            command=lambda: self.deletar_historico_selecionado(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Exportar para CSV",
            command=self.exportar_historico_csv
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Atualizar",
            command=lambda: self.atualizar_lista_historico(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Fechar",
            command=janela.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def deletar_historico_selecionado(self, tree):
        """Deleta os registros de histórico selecionados"""
        selecionados = tree.selection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione registros para deletar")
            return
            
        confirmacao = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja deletar {len(selecionados)} registro(s) selecionado(s)?",
            icon='warning'
        )
        
        if confirmacao:
            for item in selecionados:
                id_ = tree.item(item)['values'][0]
                self.banco.c.execute("DELETE FROM historico WHERE id=?", (id_,))
                self.banco.conn.commit()
                tree.delete(item)
            
            messagebox.showinfo("Sucesso", f"{len(selecionados)} registro(s) deletado(s) com sucesso!")

    def exportar_historico_csv(self):
        """Exporta o histórico para um arquivo CSV"""
        import csv
        from tkinter import filedialog
        
        try:
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
                title="Salvar Histórico como CSV"
            )
            
            if not filepath:  
                return
            
            
            registros = self.banco.obter_historico()
            cabecalho = ["ID", "Nome", "CPF", "Turma", "Data", "Item"]
            
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(cabecalho)
                writer.writerows(registros)
                
            messagebox.showinfo(
                "Sucesso", 
                f"Dados exportados com sucesso para:\n{filepath}"
            )
        except Exception as e:
            messagebox.showerror(
                "Erro", 
                f"Ocorreu um erro ao exportar:\n{str(e)}"
            )

    def atualizar_lista_historico(self, tree):
        """Atualiza a lista de histórico exibida"""
        for item in tree.get_children():
            tree.delete(item)
            
        for row in self.banco.obter_historico():
            tree.insert('', tk.END, values=row)

    def gerenciar_usuarios(self):
        """Abre a janela de gerenciamento de usuários"""
        janela = tk.Toplevel(self.root)
        janela.title("Gerenciamento de Usuários")
        janela.geometry("600x600")
        janela.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="👥 Gerenciamento de Usuários",
            font=("Segoe UI", 16, "bold"),
            bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO,
            fg=COR_TEXTO_ESCURO if modo_escuro_ativo else COR_TEXTO
        )
        title_label.pack(anchor='w', pady=(0, 10))
        
        
        tree_frame = tk.Frame(main_frame, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        tree_frame.pack(expand=True, fill=tk.BOTH)
        
        
        y_scroll = ttk.Scrollbar(tree_frame)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("id", "usuario", "senha"),
            show='headings',
            yscrollcommand=y_scroll.set
        )
        tree.pack(expand=True, fill=tk.BOTH)
        
        
        y_scroll.config(command=tree.yview)
        
        
        tree.heading("id", text="ID")
        tree.heading("usuario", text="Usuário")
        tree.heading("senha", text="Senha")
        
        
        tree.column("id", width=50, anchor='center')
        tree.column("usuario", width=200)
        tree.column("senha", width=150)
        
        
        for row in self.banco.obter_usuarios():
            tree.insert('', tk.END, values=row)
        
        
        btn_frame = tk.Frame(main_frame, bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        
        ttk.Button(
            btn_frame,
            text="Adicionar Usuário",
            command=lambda: self.adicionar_usuario(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Editar Usuário",
            command=lambda: self.editar_usuario(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Remover Usuário",
            command=lambda: self.remover_usuario(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Atualizar",
            command=lambda: self.atualizar_lista_usuarios(tree)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Fechar",
            command=janela.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def adicionar_usuario(self, tree):
        """Abre janela para adicionar novo usuário"""
        janela = tk.Toplevel(self.root)
        janela.title("Adicionar Usuário")
        janela.geometry("400x300")
        janela.resizable(False, False)
        janela.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO, 
                            padx=20, pady=20, bd=0, highlightthickness=1,
                            highlightbackground="#ddd" if not modo_escuro_ativo else COR_PRIMARIA)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="➕ Adicionar Usuário",
            font=("Segoe UI", 16, "bold"),
            bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
            fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
        )
        title_label.pack(pady=(0, 20))
        
        
        campos = ["Nome de Usuário", "Senha"]
        entradas = []
        
        for campo in campos:
            
            field_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
            field_frame.pack(fill=tk.X, pady=5)
            
            
            tk.Label(
                field_frame,
                text=campo,
                font=FONTE_PADRAO,
                bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
                fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
            ).pack(anchor='w', padx=(0, 10))
            
            
            entry = ttk.Entry(
                field_frame,
                font=FONTE_PADRAO,
                width=30,
                show="*" if campo == "Senha" else None
            )
            entry.pack(fill=tk.X, pady=2)
            entradas.append(entry)
        
        
        btn_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
        btn_frame.pack(pady=(20, 0))
        
        
        save_btn = ttk.Button(
            btn_frame,
            text="Salvar Usuário",
            command=lambda: self.salvar_novo_usuario(entradas, tree, janela)
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancelar",
            command=janela.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def salvar_novo_usuario(self, entradas, tree, janela):
        """Salva um novo usuário no banco de dados"""
        usuario = entradas[0].get().strip()
        senha = entradas[1].get().strip()
        
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!", parent=janela)
            return
            
        if len(usuario) < 4:
            messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 4 caracteres", parent=janela)
            return
            
        if len(senha) < 6:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 6 caracteres", parent=janela)
            return
        
        try:
            
            self.banco.c.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
            if self.banco.c.fetchone():
                messagebox.showerror("Erro", "Nome de usuário já existe!", parent=janela)
                return
                
            
            self.banco.criar_usuario(usuario, senha)
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!", parent=janela)
            
            
            self.atualizar_lista_usuarios(tree)
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}", parent=janela)

    def editar_usuario(self, tree):
        """Abre janela para editar usuário selecionado"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar")
            return
            
        dados = tree.item(selecionado)['values']
        
        
        if dados[1] == "admin":
            self.editar_senha_admin(dados[0])
            return
            
        janela = tk.Toplevel(self.root)
        janela.title("Editar Usuário")
        janela.geometry("500x500")
        janela.resizable(False, False)
        janela.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO, 
                            padx=20, pady=20, bd=0, highlightthickness=1,
                            highlightbackground="#ddd" if not modo_escuro_ativo else COR_PRIMARIA)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="✏️ Editar Usuário",
            font=("Segoe UI", 16, "bold"),
            bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
            fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
        )
        title_label.pack(pady=(0, 20))
        
        
        campos = ["Nome de Usuário", "Nova Senha (deixe em branco para manter a atual)"]
        entradas = []
        
        for i, campo in enumerate(campos):
            
            field_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
            field_frame.pack(fill=tk.X, pady=5)
            
            
            tk.Label(
                field_frame,
                text=campo,
                font=FONTE_PADRAO,
                bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
                fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
            ).pack(anchor='w', padx=(0, 10))
            
            
            entry = ttk.Entry(
                field_frame,
                font=FONTE_PADRAO,
                width=30,
                show="*" if "Senha" in campo else None
            )
            if i == 0:
                entry.insert(0, dados[1])  
            entry.pack(fill=tk.X, pady=2)
            entradas.append(entry)
        
        
        btn_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
        btn_frame.pack(pady=(20, 0))
        
        
        save_btn = ttk.Button(
            btn_frame,
            text="Salvar Alterações",
            command=lambda: self.salvar_edicao_usuario(dados[0], entradas, tree, janela)
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancelar",
            command=janela.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def editar_senha_admin(self, id_admin):
        """Abre janela específica para editar apenas a senha do admin"""
        janela = tk.Toplevel(self.root)
        janela.title("Alterar Senha do Admin")
        janela.geometry("400x300")
        janela.resizable(False, False)
        janela.configure(bg=COR_FUNDO_ESCURO if modo_escuro_ativo else COR_FUNDO)
        
        
        main_frame = tk.Frame(janela, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO, 
                            padx=20, pady=20, bd=0, highlightthickness=1,
                            highlightbackground="#ddd" if not modo_escuro_ativo else COR_PRIMARIA)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        
        title_label = tk.Label(
            main_frame,
            text="🔑 Alterar Senha do Admin",
            font=("Segoe UI", 16, "bold"),
            bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
            fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
        )
        title_label.pack(pady=(0, 20))
        
        
        campos = ["Nova Senha"]
        entradas = []
        
        for campo in campos:
            
            field_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
            field_frame.pack(fill=tk.X, pady=5)
            
            
            tk.Label(
                field_frame,
                text=campo,
                font=FONTE_PADRAO,
                bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO,
                fg=COR_TEXTO if not modo_escuro_ativo else COR_TEXTO_ESCURO
            ).pack(anchor='w', padx=(0, 10))
            
            
            entry = ttk.Entry(
                field_frame,
                font=FONTE_PADRAO,
                width=30,
                show="*"
            )
            entry.pack(fill=tk.X, pady=2)
            entradas.append(entry)
        
        
        btn_frame = tk.Frame(main_frame, bg="white" if not modo_escuro_ativo else COR_CARD_ESCURO)
        btn_frame.pack(pady=(20, 0))
        
        
        save_btn = ttk.Button(
            btn_frame,
            text="Salvar Senha",
            command=lambda: self.salvar_senha_admin(id_admin, entradas[0].get(), janela)
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancelar",
            command=janela.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def salvar_senha_admin(self, id_admin, nova_senha, janela):
        """Salva a nova senha do admin"""
        if not nova_senha:
            messagebox.showerror("Erro", "A senha não pode estar vazia!", parent=janela)
            return
            
        if len(nova_senha) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres!", parent=janela)
            return
            
        try:
            self.banco.atualizar_usuario(id_admin, "admin", nova_senha)
            messagebox.showinfo("Sucesso", "Senha do admin atualizada com sucesso!", parent=janela)
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}", parent=janela)

    def salvar_edicao_usuario(self, id_usuario, entradas, tree, janela):
        """Salva as alterações de um usuário editado"""
        novo_usuario = entradas[0].get().strip()
        nova_senha = entradas[1].get().strip()
        
        
        if not novo_usuario:
            messagebox.showerror("Erro", "O nome de usuário não pode estar vazio!", parent=janela)
            return
            
        if len(novo_usuario) < 4:
            messagebox.showerror("Erro", "Nome de usuário deve ter pelo menos 4 caracteres", parent=janela)
            return
            
        try:
            if nova_senha:
                if len(nova_senha) < 6:
                    messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres", parent=janela)
                    return
                self.banco.atualizar_usuario(id_usuario, novo_usuario, nova_senha)
            else:
                self.banco.atualizar_usuario(id_usuario, novo_usuario)
                
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!", parent=janela)
            
            
            self.atualizar_lista_usuarios(tree)
            janela.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nome de usuário já existe!", parent=janela)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}", parent=janela)

    def remover_usuario(self, tree):
        """Remove o usuário selecionado"""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para remover")
            return
            
        dados = tree.item(selecionado)['values']
        
        
        if dados[1] == "admin":
            messagebox.showerror("Erro", "Não é possível remover o usuário admin!")
            return
            
        confirmacao = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover o usuário {dados[1]}?",
            icon='warning'
        )
        
        if confirmacao:
            try:
                self.banco.deletar_usuario(dados[0])
                tree.delete(selecionado)
                messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def atualizar_lista_usuarios(self, tree):
        """Atualiza a lista de usuários exibida"""
        for item in tree.get_children():
            tree.delete(item)
            
        for row in self.banco.obter_usuarios():
            tree.insert('', tk.END, values=row)