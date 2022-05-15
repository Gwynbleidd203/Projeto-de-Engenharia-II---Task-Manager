from msilib.schema import Class
import sqlite3

from colorama import Cursor

from models import Tarefa, Usuario, Tipo, Status, Prioridade

# SQL

# Criação

SQL_CRIA_TAREFA = 'INSERT into TAREFA (NOME, DESCRICAO, TIPO_ID, STATUS_ID, PRIORIDADE_ID, USUARIO_ID) values (?, ?, ?, ?, ?, ?)'

SQL_CRIA_USUARIO = 'INSERT into USUARIO (USERNAME, EMAIL, SENHA) values (?, ?, ?)'

SQL_CRIA_TIPO = 'INSERT INTO TIPO (NOME) VALUES (?)'

SQL_CRIA_STATUS = 'INSERT INTO STATUS (NOME) VALUES (?)'

SQL_CRIA_PRIORIDADE = 'INSERT INTO PRIORIDADE (NOME) VALUES (?)'


# Atualização

SQL_ATUALIZA_TAREFA = 'UPDATE TAREFA SET NOME = ?, DESCRICAO = ?, TIPO_ID = ?, STATUS_ID = ?, PRIORIDADE_ID = ? WHERE ID = ?'

SQL_ATUALIZA_USUARIO = 'UPDATE USUARIO SET USERNAME = ?, EMAIL = ?, SENHA = ? where ID = ?'

SQL_ATUALIZA_TIPO = 'UPDATE TIPO SET NOME = ? WHERE ID = ?'

SQL_ATUALIZA_STATUS = 'UPDATE STATUS SET NOME = ? WHERE ID = ?'

SQL_ATUALIZA_PRIORIDADE = 'UPDATE PRIORIDADE SET NOME = ? WHERE ID = ?'

# Search

SQL_BUSCA_TAREFA = '''SELECT *, TIPO.NOME, TIPO.ID_STATUS, STATUS.NOME, STATUS.ID_STATUS, PRIORIDADE.NOME, PRIORIDADE.ID_PRIORIDADE
                      FROM TAREFA
                      INNER JOIN TIPO
                      ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                      INNER JOIN STATUS
                      ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                      INNER JOIN PRIORIDADE 
                      ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE'''

# BUSCA TAREFA POR USER
SQL_BUSCA_TAREFAS_DO_USUARIO = '''SELECT *, TIPO.NOME, TIPO.ID_TIPO, STATUS.NOME, STATUS.ID_STATUS, PRIORIDADE.NOME, PRIORIDADE.ID_PRIORIDADE
                                  FROM TAREFA
                                  INNER JOIN TIPO
                                  ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                                  INNER JOIN STATUS
                                  ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                                  INNER JOIN PRIORIDADE
                                  ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
                                  WHERE TAREFA.USUARIO_ID = ?'''

SQL_BUSCA_TIPO = 'SELECT * FROM TIPO'

SQL_BUSCA_STATUS = 'SELECT * FROM STATUS'

SQL_BUSCA_PRIORIDADE = 'SELECT * FROM PRIORIDADE'


# Search ID

SQL_BUSCA_TAREFA_POR_ID = '''SELECT *, TIPO.ID_TIPO, TIPO.NOME, STATUS.ID_STATUS, STATUS.NOME, PRIORIDADE.ID_PRIORIDADE, PRIORIDADE.NOME
                             FROM TAREFA
                             INNER JOIN TIPO
                             ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                             INNER JOIN STATUS
                             ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                             INNER JOIN PRIORIDADE
                             ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
                             WHERE TAREFA.ID = ?'''

SQL_BUSCA_TAREFA_POR_USUARIO = '''SELECT *, TIPO.ID_TIPO, TIPO.NOME, STATUS.ID_STATUS, STATUS.NOME, PRIORIDADE.ID_PRIORIDADE, PRIORIDADE.NOME
                                  FROM TAREFA
                                  INNER JOIN TIPO
                                  ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                                  INNER JOIN STATUS
                                  ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                                  INNER JOIN PRIORIDADE
                                  ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
                                  WHERE TAREFA.ID = ? AND USUARIO.ID = ?'''

SQL_USUARIO_POR_EMAIL = 'SELECT * FROM USUARIO WHERE EMAIL = ?'

SQL_BUSCA_USUARIO_POR_ID = 'SELECT * FROM USUARIO WHERE ID = ?'
# Delete

SQL_DELETA_TAREFA = 'DELETE FROM TAREFA WHERE ID = ?'


# ------------------- TAREFA -----------------------------------

class TarefaDao:
    def __init__(self, db) -> None:
        self.__db = db

    def salvar(self, tarefa):
        cursor = self.__db.cursor()

        if (tarefa._id):
            cursor.execute(SQL_ATUALIZA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id, tarefa._id))

        else:
            cursor.execute(SQL_CRIA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id, tarefa._usuario_id))
            
        self.__db.commit()
        
        return tarefa
    
    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA)
        tarefas = traduz_tarefas(cursor.fetchall())
        return tarefas
    
    
    def listar_tarefas_por_usuario(self, usuario_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFAS_DO_USUARIO, (usuario_id, ))
        tarefas = traduz_tarefas(cursor.fetchall())
        
        return tarefas
    
    
    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA_POR_ID, (id, ))
        tupla = cursor.fetchone()
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], id=tupla[0])
    
    
    def busca_por_usuario(self, id, usuario_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA_POR_USUARIO, (id, usuario_id))
        tupla = cursor.fetchone()
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], id=tupla[0])
        
    
    
    def deletar(self, id):
        self.__db.cursor().execute(SQL_DELETA_TAREFA, (id, ))
        self.__db.commit()
    
    
def traduz_tarefas(tarefas):
    def cria_tarefas_com_tupla(tupla):
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], id=tupla[0])
    return list(map(cria_tarefas_com_tupla, tarefas))


# --------------------- TIPO -------------------------------

class TipoDao:
    def __init__(self, db):
        self.__db = db
        
    
    def salvar_tipo(self, tipo):
        cursor = self.__db.cursor()
        
        if (tipo._id):
            cursor.execute(SQL_ATUALIZA_TIPO, (tipo._nome, tipo._id))
            
        else:
            cursor.execute(SQL_CRIA_TIPO, [tipo._nome])
            tipo._id = cursor.lastrowid
            
        self.__db.commit()
        
        return tipo
    
    
    def listar_tipos(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TIPO)
        tipo = traduz_tipo(cursor.fetchall())
        return tipo
 

def traduz_tipo(tipo):
    def cria_tipo_com_tupla(tupla):
        return Tipo(tupla[1], tupla[0])
    return list(map(cria_tipo_com_tupla, tipo))

# --------------------- STATUS -----------------------------

class StatusDao:
    def __init__(self, db):
        self.__db = db
    
    
    def salvar_status(self, status):
        cursor = self.__db.cursor()
        
        if (status._id):
            cursor.execute(SQL_ATUALIZA_STATUS, (status._nome, status._id))
            
        else:
            cursor.execute(SQL_CRIA_STATUS, [status._nome])
            status._id = cursor.lastrowid
        
        self.__db.commit()
        
        return status
        
    
    def listar_status(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_STATUS)
        status = traduz_status(cursor.fetchall())
        return status
    
    
def traduz_status(status):
    def cria_status_com_tupla(tupla):
        return Status(tupla[1], tupla[0])
    return list(map(cria_status_com_tupla, status))


# ------------------------------ PRIORIDADE -----------------------------------------------

class PrioridadeDao:
    def __init__(self, db):
        self.__db = db
        
    def salvar_prioridade(self, prioridade):
        cursor = self.__db.cursor()
        
        if (prioridade._id):
            cursor.exxecute(SQL_ATUALIZA_PRIORIDADE, (prioridade._nome, prioridade._id))
            
        else:
            cursor.execute(SQL_CRIA_PRIORIDADE, [prioridade._nome])
            prioridade._id = cursor.lastrowid
            
        self.__db.commit()
        
        return prioridade
    
    
    def listar_prioridades(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_PRIORIDADE)
        prioridade = traduz_prioridade(cursor.fetchall())
        return prioridade
    
    
def traduz_prioridade(prioridade):
    def cria_prioridade_com_tupla(tupla):
        return Prioridade(tupla[1], tupla[0])
    return list(map(cria_prioridade_com_tupla, prioridade))
    

# --------------------- USUARIO -----------------------------------

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
    
    
    def buscar_usuario_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario
    
def traduz_usuario(tupla):
    return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])