from flask import flash, redirect

from models import Tarefa, Usuario, Tipo, Status, Prioridade, System

import sqlite3

# ------------------------------------------------------ SQL --------------------------------------------------------------------------------------

# Criação -----------------------------------------------------------------------------------------------------------------------------------------

SQL_PRAGMA = 'PRAGMA foreign_keys=ON'

SQL_CRIA_TAREFA = '''
INSERT INTO TAREFA (NOME, DESCRICAO, TIPO_ID, STATUS_ID, PRIORIDADE_ID, USUARIO_ID, DATA_CRIACAO, DATA_TERMINO, DATA_PREVISTA)
VALUES (?, ?, ?, ?, ?, ?, CURRENT_DATE, ?, ?);
'''

SQL_CRIA_USUARIO = 'INSERT INTO USUARIO (USERNAME, EMAIL, SENHA) values (?, ?, ?)'

SQL_CRIA_TIPO = 'INSERT INTO TIPO (NOME, USUARIO_ID) VALUES (?, ?)'

SQL_CRIA_STATUS = 'INSERT INTO STATUS (NOME) VALUES (?)'

SQL_CRIA_PRIORIDADE = 'INSERT INTO PRIORIDADE (NOME) VALUES (?)'


# Atualização -----------------------------------------------------------------------------------------------------------------------------------------


SQL_ATUALIZA_TAREFA = 'UPDATE TAREFA SET NOME = ?, DESCRICAO = ?, TIPO_ID = ?, STATUS_ID = ?, PRIORIDADE_ID = ? WHERE ID = ?'

SQL_FINALIZA_TAREFA = 'UPDATE TAREFA SET STATUS_ID = 3, DATA_TERMINO = CURRENT_DATE WHERE ID = ?'

SQL_DATA_TERMINO = 'UPDATEE TAREFA SET DATA_TERMINO = CURRENT_DATE WHERE TAREFA.ID = ?'

SQL_ATUALIZA_USUARIO = 'UPDATE USUARIO SET USERNAME = ?, EMAIL = ?, SENHA = ? where ID = ?'

SQL_ATUALIZA_TIPO = 'UPDATE TIPO SET NOME = ? WHERE ID_TIPO = ?'

SQL_ATUALIZA_STATUS = 'UPDATE STATUS SET NOME = ? WHERE ID = ?'

SQL_ATUALIZA_PRIORIDADE = 'UPDATE PRIORIDADE SET NOME = ? WHERE ID = ?'


# Search -----------------------------------------------------------------------------------------------------------------------------------------


SQL_BUSCA_TAREFA = '''
SELECT TAREFA.ID, TAREFA.NOME, TAREFA.DESCRICAO, TAREFA.TIPO_ID, TAREFA.STATUS_ID, TAREFA.PRIORIDADE_ID, TAREFA.USUARIO_ID, TIPO.NOME, STATUS.NOME, PRIORIDADE.NOME,  TAREFA.DATA_CRIACAO, TAREFA.DATA_TERMINO, TAREFA.DATA_PREVISTA
FROM TAREFA
INNER JOIN TIPO
ON TAREFA.TIPO_ID = TIPO.ID_TIPO
INNER JOIN STATUS
ON TAREFA.STATUS_ID = STATUS.ID_STATUS
INNER JOIN PRIORIDADE 
ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
'''
                      
SQL_BUSCA_TAREFA_NOME = '''SELECT *
                           FROM TAREFA
                           WHERE TAREFA.NOME
                           LIKE '?'
                            '''

# BUSCA TAREFA POR USER -----------------------------------------------------------------------------------------------------------------------------------------


SQL_BUSCA_TAREFAS_DO_USUARIO = '''
SELECT TAREFA.ID, TAREFA.NOME, TAREFA.DESCRICAO, TAREFA.TIPO_ID, TAREFA.STATUS_ID, TAREFA.PRIORIDADE_ID, TAREFA.USUARIO_ID, TIPO.NOME, STATUS.NOME, PRIORIDADE.NOME, TAREFA.DATA_CRIACAO, TAREFA.DATA_TERMINO, TAREFA.DATA_PREVISTA
FROM TAREFA
INNER JOIN TIPO
ON TAREFA.TIPO_ID = TIPO.ID_TIPO
INNER JOIN STATUS
ON TAREFA.STATUS_ID = STATUS.ID_STATUS
INNER JOIN PRIORIDADE
ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
WHERE TAREFA.USUARIO_ID = ? AND STATUS.ID_STATUS <> 3
'''

    

SQL_BUSCA_TAREFAS_FEITAS = '''
SELECT TAREFA.ID, TAREFA.NOME, TAREFA.DESCRICAO, TAREFA.TIPO_ID, TAREFA.STATUS_ID, TAREFA.PRIORIDADE_ID, TAREFA.USUARIO_ID, TIPO.NOME, STATUS.NOME, PRIORIDADE.NOME, TAREFA.DATA_CRIACAO, TAREFA.DATA_TERMINO, TAREFA.DATA_PREVISTA
FROM TAREFA
INNER JOIN TIPO
ON TIPO.ID_TIPO = TAREFA.TIPO_ID
INNER JOIN STATUS
ON STATUS.ID_STATUS = TAREFA.STATUS_ID
INNER JOIN PRIORIDADE
ON PRIORIDADE.ID_PRIORIDADE = TAREFA.PRIORIDADE_ID
WHERE TAREFA.USUARIO_ID = ? AND STATUS.ID_STATUS = 3'''

SQL_BUSCA_TIPO = 'SELECT * FROM TIPO'

SQL_BUSCA_TIPO_POR_USUARIO = 'SELECT * FROM TIPO WHERE USUARIO_ID = ? OR USUARIO_ID = 0'

SQL_BUSCA_TIPOS_DO_USUARIO = 'SELECT * FROM TIPO WHERE TIPO.USUARIO_ID = ?'

SQL_BUSCA_STATUS = 'SELECT * FROM STATUS'

SQL_BUSCA_PRIORIDADE = 'SELECT * FROM PRIORIDADE'


# Search ID -----------------------------------------------------------------------------------------------------------------------------------------

SQL_BUSCA_TAREFA_POR_ID = '''
SELECT TAREFA.ID, TAREFA.NOME, TAREFA.DESCRICAO, TAREFA.TIPO_ID, TAREFA.STATUS_ID, TAREFA.PRIORIDADE_ID, TAREFA.USUARIO_ID, TIPO.NOME, STATUS.NOME, PRIORIDADE.NOME,  TAREFA.DATA_CRIACAO, TAREFA.DATA_TERMINO, TAREFA.DATA_PREVISTA
FROM TAREFA
INNER JOIN TIPO
ON TAREFA.TIPO_ID = TIPO.ID_TIPO
INNER JOIN STATUS
ON TAREFA.STATUS_ID = STATUS.ID_STATUS
INNER JOIN PRIORIDADE
ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
WHERE TAREFA.ID = ?
'''

SQL_BUSCA_TIPO_POR_ID= 'SELECT * FROM TIPO WHERE TIPO.ID_TIPO = ?'

SQL_BUSCA_TAREFA_POR_USUARIO = '''
SELECT TAREFA.ID, TAREFA.NOME, TAREFA.DESCRICAO, TAREFA.TIPO_ID, TAREFA.STATUS_ID, TAREFA.PRIORIDADE_ID, TAREFA.USUARIO_ID, TIPO.NOME, STATUS.NOME, PRIORIDADE.NOME,  TAREFA.DATA_CRIACAO, TAREFA.DATA_TERMINO, TAREFA.DATA_PREVISTA
FROM TAREFA
INNER JOIN TIPO
ON TAREFA.TIPO_ID = TIPO.ID_TIPO
INNER JOIN STATUS
ON TAREFA.STATUS_ID = STATUS.ID_STATUS
INNER JOIN PRIORIDADE
ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
WHERE TAREFA.ID = ? AND TAREFA.USUARIO_ID = ?
'''

SQL_USUARIO_POR_EMAIL = 'SELECT * FROM USUARIO WHERE EMAIL = ?'

SQL_BUSCA_USUARIO_POR_ID = 'SELECT * FROM USUARIO WHERE ID = ?'


# Delete -----------------------------------------------------------------------------------------------------------------------------------------


SQL_DELETA_TAREFA = 'DELETE FROM TAREFA WHERE ID = ?'

SQL_DELETA_TIPO = 'DELETE FROM TIPO WHERE ID_TIPO = ?'


# User Profile -----------------------------------------------------------------------------------------------------------------------------------------

SQL_CONTA_TAREFAS = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = ?'

SQL_CONTA_TAREFAS_FEITAS = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = ? AND TAREFA.STATUS_ID = 3'

SQL_CONTA_TAREFAS_FAZENDO = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = ? AND TAREFA.STATUS_ID = 2'

SQL_CONTA_TAREFAS_FAZER = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = ? AND TAREFA.STATUS_ID = 1'

# -------------------- Trigger Try -----------------------------

SQL_DELETA_USER_ALL = '''DELIMITER //
                         CREATE TRIGGER deleteAll
                         AFTER DELETE ON USARIO
                         FOR EACH ROW
                         BEGIN
                         DELETE FROM TAREFA WHERE USUARIO_ID = OLD.ID
                         DELETE FROM TIPO WHERE USUARIO_ID = OLD.ID
                         END
                         //
                         DELIMITER ;'''


# ------------------- TAREFA -----------------------------------

class TarefaDao:
    def __init__(self, db) -> None:
        self.__db = db

    def salvar(self, tarefa:Tarefa):
        cursor = self.__db.cursor()

        if (tarefa._id):
            cursor.execute(SQL_ATUALIZA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id, tarefa._id))

        else:
            cursor.execute(SQL_CRIA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id, tarefa._usuario_id, tarefa._data_criacao, tarefa._data_prevista))
            
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

    def listar_tarefas_finalizadas_usuario(self, usuario_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFAS_FEITAS, (usuario_id, ))
        tarefas = traduz_tarefas(cursor.fetchall())

        return tarefas
    
    
    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA_POR_ID, (id, ))
        tupla = cursor.fetchone()
        return Tarefa(nome=tupla[1], descricao=tupla[2], tipo_id=tupla[3], status_id=tupla[4], prioridade_id=tupla[5], usuario_id=tupla[6], tipo=tupla[7], status=tupla[8], prioridade=tupla[9], data_criacao=tupla[10], data_termino=tupla[11], data_prevista=tupla[12], id=tupla[0])
    
    
    def busca_por_usuario(self, id, usuario_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA_POR_USUARIO, (id, usuario_id))
        tupla = cursor.fetchone()
        return Tarefa(nome=tupla[1], descricao=tupla[2], tipo_id=tupla[3], status_id=tupla[4], prioridade_id=tupla[5], usuario_id=tupla[6], tipo=tupla[7], status=tupla[8], prioridade=tupla[9], data_criacao=tupla[10], data_termino=tupla[11], data_prevista=tupla[12], id=tupla[0])
    
    
    def busca_por_nome(self, nome):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TAREFA_NOME, (nome, ))
        tarefas = traduz_tarefas(cursor.fetchall())
        
        return tarefas


    def finaliza_tarefa(self, tarefa:Tarefa):
        cursor = self.__db.cursor()
        cursor.execute(SQL_FINALIZA_TAREFA, (tarefa._data_termino, tarefa._id))

        self.__db.commit()

        return tarefa
        
        
    def deletar(self, id):
        self.__db.cursor().execute(SQL_DELETA_TAREFA, (id, ))
        self.__db.commit()
    
    
def traduz_tarefas(tarefas):
    def cria_tarefas_com_tupla(tupla):
        return Tarefa(nome=tupla[1], descricao=tupla[2], tipo_id=tupla[3], status_id=tupla[4], prioridade_id=tupla[5], usuario_id=tupla[6], tipo=tupla[7], status=tupla[8], prioridade=tupla[9], data_criacao=tupla[10], data_termino=tupla[11], data_prevista=tupla[12], id=tupla[0])
    return list(map(cria_tarefas_com_tupla, tarefas))


# --------------------- TIPO -------------------------------

class TipoDao:
    def __init__(self, db):
        self.__db = db
        
    
    def salvar_tipo(self, tipo:Tipo):
        cursor = self.__db.cursor()
        
        if (tipo._id):
            cursor.execute(SQL_ATUALIZA_TIPO, (tipo._nome, tipo._id))
            
        else:
            cursor.execute(SQL_CRIA_TIPO, (tipo._nome, tipo._usuario_id))
            tipo._id = cursor.lastrowid
            
        self.__db.commit()
        
        return tipo
    
    
    def listar_tipos(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TIPO)
        tipo = traduz_tipo(cursor.fetchall())
        return tipo


    def listar_tipo_usuario(self, usuario_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TIPO_POR_USUARIO, (usuario_id, ))
        tipo = traduz_tipo(cursor.fetchall())
        return tipo

    
    def listar_tipos_do_usuario(self, usuario_id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TIPOS_DO_USUARIO, (usuario_id, ))
        tipo = traduz_tipo(cursor.fetchall())
        return tipo


    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_TIPO_POR_ID, (id, ))
        tupla = cursor.fetchone()
        return Tipo(tupla[1], tupla[2], id=tupla[0])


    def deletar_tipo(self, id):
        self.__db.cursor().execute(SQL_DELETA_TIPO, (id, ))
        self.__db.commit()
 

def traduz_tipo(tipo):
    def cria_tipo_com_tupla(tupla):
        return Tipo(tupla[1], tupla[2], tupla[0])
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
        return Prioridade(tupla[1], id=tupla[0])
    return list(map(cria_prioridade_com_tupla, prioridade))
    

# --------------------- USUARIO -----------------------------------

class UsuarioDao:
    def __init__(self, db) -> None:
        self.__db = db
        
    def salvar_usuario(self, usuario):
        cursor = self.__db.cursor()

        try:
        
            if (usuario._id):
                cursor.execute(SQL_ATUALIZA_USUARIO, (usuario._nome, usuario._email, usuario._senha, usuario._id))
                
            else:
                cursor.execute(SQL_CRIA_USUARIO, (usuario._nome, usuario._email, usuario._senha))
                
            self.__db.commit()

            return usuario

        except sqlite3.IntegrityError:

            flash(u'Email já cadastrado! Tente logar usando-o ou crie uma nova conta.', 'msg-ul-bad')


        except Exception:

            flash(u'Erro desconhecido ao criar/atualizar conta! Tente novamente mais tarde.', 'msg-ul-bad')

        return redirect('/')


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
    
    # Tentar otimizar o resultado
    def conta_tarefas(self, usuario_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_CONTA_TAREFAS, (usuario_id,))
            tarefas_qnt = cursor.fetchone()

            return tarefas_qnt

        except Exception:

            return 0
    
    def conta_tarefas_prontas(self, usuario_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_CONTA_TAREFAS_FEITAS, (usuario_id,))
            tarefas_prontas = cursor.fetchone()

            return tarefas_prontas
        
        except Exception:

            return 0
        
    
    def conta_tarefas_fazer(self, usuario_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_CONTA_TAREFAS_FAZER, (usuario_id,))
            tarefas_fazer = cursor.fetchone()

            return tarefas_fazer

        except Exception:

            return 0
        
    
    def conta_tarefas_fazendo(self, usuario_id):
        cursor = self.__db.cursor()
        try:
            cursor.execute(SQL_CONTA_TAREFAS_FAZENDO, (usuario_id,))
            tarefas_fazendo = cursor.fetchone()
            
            return tarefas_fazendo
        
        except Exception:

            return 0
    
def traduz_usuario(tupla):
    return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])