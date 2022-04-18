from flask import Flask, render_template, request, redirect, session, flash

from dao import TarefaDao, UsuarioDao

from models import Tarefa, Usuario

import sqlite3


app = Flask(__name__)
app.secret_key = 'ENGII'

db = sqlite3.connect('banco.db', check_same_thread=False)

# dao

tarefa_dao = TarefaDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    proxima = request.args.get('proxima')
    lista = tarefa_dao.listar()

    return render_template('index.html', proxima=proxima, tarefas=lista)


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

    tarefa = Tarefa(nome, descricao, tipo, status, prioridade)
    
    tarefa = tarefa_dao.salvar(tarefa)

    return redirect('/sobre')


@app.route('/criar_usuario', methods=['POST', ])
def criar_usuario():
    username = request.form['username']
    email = request.form['email']
    senha = request.form['senha']
    
    usuario = Usuario(username, email, senha)
    
    usuario_dao.salvar_usuario(usuario)
    
    return redirect('/')


@app.route('/editar_tarefa')
def editar_tarefa():
    
    return redirect('/')


@app.route('/lista_de_tarefas')
def lista_de_tarefas():
    lista = tarefa_dao.listar()
    
    return render_template('index.html', tarefas=lista)


@app.route('/tarefa_info/<int:id>')
def tarefa_info(id):
    tarefa = tarefa_dao.busca_por_id(id)
    
    return render_template('tarefa_info.html', tarefa=tarefa)


@app.route('/deletar_tarefa/<int:id>')
def deletar_tarefa(id):
    tarefa_dao.deletar(id)
    
    return redirect('/')


@app.route('/status')
def status():

    return render_template('status.html')


@app.route('/sobre')
def sobre():

    return render_template('sobre.html')


if __name__ == '__main__':

    app.run(debug=True)