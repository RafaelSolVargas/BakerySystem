from conexoes import *

def Acessar_Adm():
    pass


def Cadastrar_Produto(codigo, nome, preco, quantidade):
    with Conectar('padaria.db') as (conn, cursor):
        cursor.execute(
            'INSERT INTO estoque (codigo, nome, preco, quant) VALUES (?, ?, ?, ?)',
        (codigo, nome, preco, quantidade))
        conn.commit()


def Atualizar_Produto():
    pass


def Adicionar_User(login, senha):
    with Conectar('padaria.db') as (conn, cursor):
        cursor.execute(
            'INSERT INTO usuarios (login, senha) VALUES (?, ?)',
        (login, senha))
        conn.commit()


def Buscar_Produto(codigo):
    with Conectar('padaria.db') as (conn, cursor):
        cursor.execute('SELECT codigo, nome, quant, preco FROM estoque WHERE codigo = ?', (codigo,))
        conn.commit()

        return cursor.fetchone()
