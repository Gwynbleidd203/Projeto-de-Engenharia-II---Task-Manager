class Usuario:
    def __init__(self, nome, email, senha, id=None):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha

class Tarefa:
    def __init__(self, nome, descricao, tipo_id, status_id, prioridade_id, tipo, status, prioridade, usuario_id, data_prevista, data_criacao, data_termino=None, id=None):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._tipo_id = tipo_id
        self._status_id = status_id
        self._prioridade_id = prioridade_id
        self._tipo = tipo
        self._status = status
        self._prioridade = prioridade
        self._usuario_id = usuario_id
        self._data_criacao = data_criacao
        self._data_termino = data_termino
        self._data_prevista = data_prevista


class Tipo:
    def __init__(self, nome, usuario_id, id=None):
        self._id = id
        self._nome = nome
        self._usuario_id = usuario_id
        


class Status:
    def __init__(self, nome, id=None):
        self._id = id
        self._nome = nome
     
        
class Prioridade:
    def __init__(self, nome, id=None):
        self._id = id
        self._nome = nome
