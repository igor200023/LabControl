import sqlite3
from config import *

class BancoDeDados:
    def __init__(self):
        self.conn = sqlite3.connect('DB/labcontrol.db')
        self.c = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, cpf TEXT, turma TEXT, data TEXT, item TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, cpf TEXT, turma TEXT, data TEXT, item TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT, senha TEXT)''')
        
        
        self.c.execute("SELECT id FROM usuarios WHERE usuario = 'admin' ORDER BY id")
        admins = self.c.fetchall()
        if len(admins) > 1:
            for admin_id in admins[1:]:
                self.c.execute("DELETE FROM usuarios WHERE id = ?", (admin_id[0],))
        
        
        self.c.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
        if not self.c.fetchone():
            self.c.execute("INSERT INTO usuarios (usuario, senha) VALUES ('admin', 'admin')")
        
        self.conn.commit()

    def verificar_login(self, usuario, senha):
        self.c.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        user = self.c.fetchone()
        return user is not None

    def criar_usuario(self, usuario, senha):
        self.c.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        self.conn.commit()

    def inserir_emprestimo(self, nome, cpf, turma, data, item):
        self.c.execute("INSERT INTO emprestimos (nome, cpf, turma, data, item) VALUES (?, ?, ?, ?, ?)",
                     (nome, cpf, turma, data, item))
        self.conn.commit()

    def obter_emprestimos(self):
        return self.c.execute("SELECT * FROM emprestimos").fetchall()

    def atualizar_emprestimo(self, id_, nome, cpf, turma, data, item):
        self.c.execute("UPDATE emprestimos SET nome=?, cpf=?, turma=?, data=?, item=? WHERE id=?",
                     (nome, cpf, turma, data, item, id_))
        self.conn.commit()

    def deletar_emprestimo(self, id_):
        self.c.execute("DELETE FROM emprestimos WHERE id=?", (id_,))
        self.conn.commit()

    def dar_baixa(self, id_, nome, cpf, turma, data, item):
        self.deletar_emprestimo(id_)
        self.c.execute("INSERT INTO historico (nome, cpf, turma, data, item) VALUES (?, ?, ?, ?, ?)",
                     (nome, cpf, turma, data, item))
        self.conn.commit()

    def obter_historico(self):
        return self.c.execute("""
            SELECT * FROM historico
            ORDER BY substr(data, 7, 4) || '-' || substr(data, 4, 2) || '-' || substr(data, 1, 2) DESC
        """).fetchall()

    def obter_usuarios(self):
        return self.c.execute("SELECT * FROM usuarios").fetchall()

    def atualizar_usuario(self, id_, usuario, senha=None):
        if senha:
            self.c.execute("UPDATE usuarios SET usuario=?, senha=? WHERE id=?", (usuario, senha, id_))
        else:
            self.c.execute("UPDATE usuarios SET usuario=? WHERE id=?", (usuario, id_))
        self.conn.commit()

    def deletar_usuario(self, id_):
        self.c.execute("DELETE FROM usuarios WHERE id=?", (id_,))
        self.conn.commit()

    def close(self):
        self.conn.close()

class Usuario:
    def __init__(self, banco: BancoDeDados):
        self.banco = banco

    def verificar_login(self, usuario, senha):
        return self.banco.verificar_login(usuario, senha)

    def criar_usuario(self, usuario, senha):
        self.banco.criar_usuario(usuario, senha)