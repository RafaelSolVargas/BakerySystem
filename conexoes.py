import sqlite3
from contextlib import contextmanager
from datetime import datetime
from sqlite3.dbapi2 import Error
import bcrypt

databasePath = 'padaria.db'


@contextmanager
def Conectar(databasePath):
    try:
        conn = sqlite3.connect(databasePath)
        cursor = conn.cursor()
        yield conn, cursor

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def Verificar_Codigo(codigo, quant):
    """
    Verifica se um código entregue como parâmetro está cadastrado no Estoque, e se existe
    uma quantidade suficiente no estoque para efetuar a compra da quantidade pedida, caso seja possível,
    irá retorna True, caso não seja retorna False. Caso exista múltiplos produtos com o 
    mesmo código cadastrado levanta um ValueError alertando a duplicação de códigos ou que 
    não tem produtos suficientes em estoque
    """
    with Conectar('padaria.db') as (conn, cursor):
        cursor.execute(
            f'SELECT codigo, quant FROM estoque WHERE codigo = ({codigo})')
        conn.commit()

        retornos = cursor.fetchall()

        if len(retornos) == 0:
            return False
        elif len(retornos) == 1 and retornos[0][1] >= int(quant):
            return True
        else:
            raise ValueError(
                "ERRO: Existem códigos duplicados")


def Add_Historico(produtos):
    """
    Recebe uma lista de produtos que foram vendidos para adicionar no histórico de vendas, será armazenado
    o codigo, nome, data, quantidade e valor total. A data é criada automaticamente pelo Database, 
    Cada produto dentro da lista de produtos deve ser um array ou tupla com as seguintes informações 
    Na respectiva ordem: codigo, nome, quant, valorTot
    """
    with Conectar(databasePath) as (conn, cursor):
        data = datetime.today().strftime('%Y-%m-%d %H:%M')

        for produto in produtos:
            cursor.execute(
                f'INSERT INTO historico (codigo, nome, data, quant, valor) VALUES (?, ?, ?, ?, ?)', (produto[0], produto[1], data, produto[2], produto[3]))
        conn.commit()


def Remover_Estoque(produtos):
    """
    Irá diminuir a quantidade de cada produto após uma venda ser concluída
    O array de cada produto deve seguir a seguinte ordem: 
    codigo, quantidade 
    """
    with Conectar(databasePath) as (conn, cursor):

        for produto in produtos:
            cursor.execute(
                f'UPDATE estoque SET quant=(quant - ?) WHERE codigo=?', (int(produto[2]), int(produto[0])))

        conn.commit()


def Carregar_Produto(codigo):
    """
    Recebe um codigo e retorna uma tupla com os dados desse produto cadastrados no estoque,
    Na seguinte ordem: codigo(int), nome(str), valorUnit(float), quantidade(int)
    """
    with Conectar(databasePath) as (conn, cursor):
        cursor.execute(
            f'SELECT codigo, nome, preco, quant FROM estoque WHERE codigo = {codigo}')
        conn.commit()

        retorno = cursor.fetchall()
        if len(retorno) == 1:
            return retorno[0]
        else:
            raise ValueError("Produto não encontrado ou duplicado no Estoque")


def Buscar_Historico():
    """
    Retorna uma lista com tuplas, contendo todos os cadastros de vendas no historico, as tuplas
    seguem a seguinte ordem: id, codigo, nome, data, quant, valorTot
    """
    with Conectar(databasePath) as (conn, cursor):
        cursor.execute('SELECT * FROM historico')
        conn.commit()

        return cursor.fetchall()


def Buscar_Estoque():
    """
    Retorna uma lista com tuplas, cada tupla possui as informações de um produto no estoque
    as tuplas seguem a seguinte ordem: codigo, nome, quant, precoUnit
    """
    with Conectar(databasePath) as (conn, cursor):
        cursor.execute('SELECT codigo, nome, quant, preco FROM estoque')
        conn.commit()

        return cursor.fetchall()


def Verificar_User(login, senha):
    """
    Verifica se o login e senha passados estão cadastrados como usuários, retorna True caso encontre
    um cadastro em que o login e senha passados batam com o registro, retorna False caso não encontre
    nenhum caso que os dados batam, a senha deve ser passada como string
    """
    with Conectar(databasePath) as (conn, cursor):
        senha_byte = str.encode(senha)

        cursor.execute(
            f'SELECT login, senha FROM usuarios WHERE login=?', (login,))
        retornos = cursor.fetchall()
        conn.commit()

        for user in retornos:
            if bcrypt.checkpw(senha_byte, user[1]):
                return True
        return False


def Cadastrar_User(login, senha):
    """
    Essa função irá adicionar um usuário na tabela, para isso é necessário que seja passado o login e a senha
    em string, a senha em si será criptgrafada antes de ser guardada (fonte: https://zetcode.com/python/bcrypt/) 
    """
    senha_byte = str.encode(senha)
    hashed = bcrypt.hashpw(senha_byte, bcrypt.gensalt())

    with Conectar(databasePath) as (conn, cursor):
        cursor.execute(
            'INSERT INTO usuarios (login, senha) VALUES (?, ?)', (login, hashed))
        conn.commit()


def Cadastrar_Produto(codigo, nome, preco, quantidade):
    with Conectar(databasePath) as (conn, cursor):
        cursor.execute(
            'INSERT or IGNORE INTO estoque (codigo, nome, preco, quant) VALUES (?, ?, ?, ?)',
            (codigo, nome, preco, quantidade))
        conn.commit()


def Atualizar_Produto(codigo, nome, preco, quantidade):
    with Conectar(databasePath) as (conn, cursor):
        cursor.execute(
            'UPDATE estoque SET nome = ?, preco = ?, quant = ? WHERE codigo = ?',
            (nome, preco, quantidade, codigo))
        conn.commit()


def Buscar_Produto(codigo):
    with Conectar(databasePath) as (conn, cursor):
        cursor.execute(
            'SELECT codigo, nome, quant, preco FROM estoque WHERE codigo = ?', (codigo,))
        conn.commit()

        # Retorna uma tupla com os dados na ordem codigo, nome, quant e preco
        return cursor.fetchone()
