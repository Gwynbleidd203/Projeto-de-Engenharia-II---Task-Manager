class Tarefa:
    def __init__(self, nome, descricao, tipo, status, prioridade, id=None):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._tipo = tipo
        self._status = status
        self._prioridade = prioridade
       

class Usuario:
    def __init__(self, nome, email, senha, id=None):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha

