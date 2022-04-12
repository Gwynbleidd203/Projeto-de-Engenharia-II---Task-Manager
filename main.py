from flask import Flask, render_template, request, redirect, session, flash

from dao import TarefaDao

from models import Tarefa, Usuario

## KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW KEKW K

#import sqlite3
#db = sqlite3.connect('banco.db')
#cursor = db.cursor().execute('select 1')
#print(cursor)




app = Flask(__name__)
app.secret_key = 'ENGII'


@app.route('/')
def index():
    proxima = request.args.get('proxima')

    return render_template('index.html', proxima=proxima)


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

    TarefaDao.salvar(tarefa)


    return redirect('/sobre')


@app.route('/status')
def status():

    return render_template('status.html')


@app.route('/sobre')
def sobre():

    return render_template('sobre.html')


if __name__ == '__main__':

    app.run(debug=True)