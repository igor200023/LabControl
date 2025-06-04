Documentação do Sistema LabControl
Estrutura e Recursos do Sistema
Linguagem de Programação: Python

Interface Gráfica (GUI): Tkinter

Banco de Dados: SQLite

Bibliotecas Necessárias
pip install Pillow

Observação:
O projeto inclui um executável independente (gerado com PyInstaller).

Visão Geral do Sistema
Nome do Projeto: LabControl

Principais Funcionalidades:
Modo Escuro – Melhora a adaptação do usuário.

Controle de Administrador – Funções críticas restritas:

Gerenciamento de usuários (criar, excluir, alterar senhas).

Cadastro de Usuários – Permite que novos usuários se registrem.

Validação de Login e Senha – Autenticação segura.

Gestão de Empréstimos:

Registrar novos empréstimos.

Visualizar empréstimos ativos (com opções de editar, excluir ou marcar como devolvido).

Acessar histórico de empréstimos (exportável para CSV, com possibilidade de exclusão).

Interface do Usuário e Fluxo de Trabalho
Página Inicial
Três botões principais de interação:

Registrar Empréstimo

Abre um formulário com os campos:

Nome do Aluno

CPF

Turma

Data do Empréstimo

Item Emprestado

Empréstimos em Andamento

Exibe uma lista de empréstimos ativos com os seguintes dados:

Nome do Aluno | CPF | Turma | Data do Empréstimo | Item Emprestado

Ações disponíveis para cada registro:

Editar dados

Excluir registro

Dar baixa (marca como devolvido e envia para o histórico)

Histórico de Devoluções

Lista todos os empréstimos já finalizados (marcados como devolvidos).

Campos exibidos:

Nome do Aluno | CPF | Turma | Data do Empréstimo | Item Emprestado

Opção de exportação: Gerar relatório em CSV.

Observações Adicionais
Ao dar baixa em um empréstimo, os dados são transferidos automaticamente para o histórico.

O administrador tem acesso total, enquanto usuários comuns têm permissões limitadas.

login de teste:admin
senha de teste:admin