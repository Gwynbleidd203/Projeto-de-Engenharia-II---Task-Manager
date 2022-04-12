from models import Tarefa, Usuario

import sqlite3

db = sqlite3.connect('banco.db', check_same_thread=False)
cursor = db.cursor()

# SQL

# Criação
SQL_CRIA_TAREFA = 'INSERT into TAREFA (NOME, DESCRICAO, TIPO, STATUS, PRIORIDADE) values (?, ?, ?, ?, ?)'

# Atualização
SQL_ATUALIZA_TAREFA = 'UPDATE TAREFA SET NOME = ?, DESCRICAO = ?, TIPO = ?, STATUS = ?, PRIORIDADE = ? where ID = ?'

class TarefaDao:


    def salvar(tarefa):
        cursor = db.cursor()

        if (tarefa._id):
            cursor.execute(SQL_ATUALIZA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo, tarefa._status, tarefa._prioridade))

        else:
            cursor.execute(SQL_CRIA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo, tarefa._status, tarefa._prioridade))
            

        db.commit()
        return tarefa