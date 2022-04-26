class Tarefa:
    def __init__(self, nome, descricao, tipo_id, status_id, prioridade_id, id=None):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._tipo_id = tipo_id
        self._status_id = status_id
        self._prioridade_id = prioridade_id
       

class Usuario:
    def __init__(self, nome, email, senha, id=None):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha

