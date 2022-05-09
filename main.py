from flask import Flask, render_template, request, redirect, session, flash

from dao import StatusDao, TarefaDao, TipoDao, UsuarioDao, PrioridadeDao

from werkzeug.security import check_password_hash, generate_password_hash

from models import Prioridade, Tarefa, Usuario

import sqlite3


app = Flask(__name__)
app.secret_key = 'ENGII'

db = sqlite3.connect('banco.db', check_same_thread=False)

# dao

tarefa_dao = TarefaDao(db)
usuario_dao = UsuarioDao(db)
tipo_dao = TipoDao(db)
status_dao = StatusDao(db)
prioridade_dao = PrioridadeDao(db)


@app.route('/')
def index():
    proxima = request.args.get('proxima')
    lista = tarefa_dao.listar()
    tipos = tipo_dao.listar_tipos()
    lista_status = status_dao.listar_status()
    lista_prioridades = prioridade_dao.listar_prioridades()

    return render_template('index.html', proxima=proxima, tarefas=lista, tipos=tipos , status_list=lista_status, prioridades=lista_prioridades)


@app.route('/autenticar')
def autenticar():

    return redirect('/')


@app.route('/novo')
def novo():

    return render_template('novo.html')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    tipo = request.form['tipo']
    status = request.form['status']
    prioridade = request.form['prioridade']

    tarefa = Tarefa(nome, descricao, tipo, status, prioridade, None, None)
    
    tarefa = tarefa_dao.salvar(tarefa)

    return redirect('/')


@app.route('/editar_tarefa/<int:id>')
def editar_tarefa(id):
    tarefa = tarefa_dao.busca_por_id(id)
    tipos = tipo_dao.listar_tipos()
    lista_status = status_dao.listar_status()
    lista_prioridade = prioridade_dao.listar_prioridades()
    
    return render_template('/tarefa_edit.html', tarefa=tarefa, tipos=tipos , status_list=lista_status, prioridades=lista_prioridade)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    tipo_id = request.form['tipo']
    status_id = request.form['status']
    prioridade_id = request.form['prioridade']
    id = request.form['id']

    tarefa = Tarefa(nome, descricao, tipo_id, status_id, prioridade_id, None, None, id)

    tarefa_dao.salvar(tarefa)

    return redirect('/')


@app.route('/lista_de_tarefas')
def lista_de_tarefas():
    lista = tarefa_dao.listar()
    
    return render_template('index.html', tarefas=lista)


@app.route('/tarefa_info/<int:id>')
def tarefa_info(id):
    lista = tarefa_dao.busca_por_id(id)
    
    return render_template('tarefa_info.html', tarefa=lista)


@app.route('/deletar_tarefa/<int:id>')
def deletar_tarefa(id):
    tarefa_dao.deletar(id)
    
    return redirect('/')

# USUARIO

@app.route('/criar_usuario', methods=['POST', ])
def criar_usuario():
    username = request.form['username']
    email = request.form['email']
    senha = request.form['senha']
    
    usuario = Usuario(username, email, senha)
    
    usuario_dao.salvar_usuario(usuario)
    
    return redirect('/')


@app.route('/login')
def login():
    proxima=request.args.get('proxima')
    if proxima == None:
        proxima=''
    return render_template('index.html', proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar_usu():
    usuario = usuario_dao.buscar_por_email_usu(request.form['email'])
    if usuario:
        if usuario._senha == request.form['senha']:
            session ['usuario_logado'] = request.form['email']
            flash(request.form['email']+ 'Logou com sucesso')
            u = usuario._nome
            return redirect('/', user = u)


    flash('Não logado, tente novamente')
    return  redirect('/')           


@app.route('/status')
def status():

    return render_template('status.html')


@app.route('/sobre')
def sobre():

    return render_template('sobre.html')



if __name__ == '__main__':

    app.run(debug=True)
