import sqlite3

from models import Tarefa, Usuario

# SQL

# Criação
SQL_CRIA_TAREFA = 'INSERT into TAREFA (NOME, DESCRICAO, TIPO_ID, STATUS_ID, PRIORIDADE_ID) values (?, ?, ?, ?, ?)'

SQL_CRIA_USUARIO = 'INSERT into USUARIO (USERNAME, EMAIL, SENHA) values (?, ?, ?)'

# Atualização
SQL_ATUALIZA_TAREFA = 'UPDATE TAREFA SET NOME = ?, DESCRICAO = ?, TIPO = ?, STATUS = ?, PRIORIDADE = ? where ID = ?'

SQL_ATUALIZA_USUARIO = 'UPDATE USUARIO SET USERNAME = ?, EMAIL = ?, SENHA = ? where ID = ?'

# Search

SQL_BUSCA_TAREFA = 'SELECT * FROM TAREFA'

# Search ID

SQL_BUSCA_TAREFA_POR_ID = 'SELECT * FROM TAREFA WHERE ID = ?'
SQL_USUARIO_POR_EMAIL = 'SELECT * FROM USUARIO WHERE EMAIL = ?'

# Delete

SQL_DELETA_TAREFA = 'DELETE FROM TAREFA WHERE ID = ?'


class TarefaDao:
    def __init__(self, db) -> None:
        self.__db = db

    def salvar(self, tarefa):
        cursor = self.__db.cursor()

        if (tarefa._id):
            cursor.execute(SQL_ATUALIZA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id, tarefa._id))

        else:
            cursor.execute(SQL_CRIA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id))
            cursor_id = cursor.lastrowid
            tarefa._id = cursor_id

        self.__db.commit()
        return tarefa
    
    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA)
        tarefas = traduz_tarefas(cursor.fetchall())
        return tarefas
    
    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA_POR_ID, (id, ))
        tupla = cursor.fetchone()
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])
    
    def deletar(self, id):
        self.__db.cursor().execute(SQL_DELETA_TAREFA, (id, ))
        self.__db.commit()
    
    
def traduz_tarefas(tarefas):
    def cria_tarefas_com_tupla(tupla):
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], id=tupla[0])
    return list(map(cria_tarefas_com_tupla, tarefas))


def traduz_usuario(tupla):
    return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])
    

class UsuarioDao:
    def __init__(self, db) -> None:
        self.__db = db
        
    def salvar_usuario(self, usuario):
        cursor = self.__db.cursor()
        
        if (usuario._id):
            cursor.execute(SQL_ATUALIZA_USUARIO, (usuario._nome, usuario._email, usuario._senha, usuario._id))
            
        else:
            cursor.execute(SQL_CRIA_USUARIO, (usuario._nome, usuario._email, usuario._senha))
            
        self.__db.commit()
        return usuario

    def buscar_por_email_usu(self, email):
        cursor =  self.__db.cursor()
        cursor.execute(SQL_USUARIO_POR_EMAIL, (email,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario