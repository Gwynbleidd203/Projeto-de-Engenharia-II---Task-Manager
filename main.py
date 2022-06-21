from flask import Flask, render_template, request, redirect, session, flash

from dao import StatusDao, TarefaDao, TipoDao, UsuarioDao, PrioridadeDao

from werkzeug.security import check_password_hash, generate_password_hash

from models import Tarefa, Usuario, Tipo

from functools import wraps

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

# Login required function ------------------------------------------------

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario_logado' not in session or session['usuario_logado'] == None:
            
            return f(*args, **kwargs)
        
        else:
            flash(u"Você necessita de login para acessar essa página", "msg-ul-bad")
            
            return redirect('/login')
        
    return wrap

# --------------------------------------------------------------------------


@app.route('/')
def index():
    if session == None or "":
        proxima = request.args.get('proxima')
    
        return render_template('landing.html', proxima=proxima)
    
    if session:
        try:
            usuario = usuario_dao.buscar_usuario_por_id(session['usuario_logado'])
            print(session['usuario_logado'])
            proxima = request.args.get('proxima')
            lista = tarefa_dao.listar_tarefas_por_usuario(usuario._id)
            lista_tipo = tipo_dao.listar_tipo_usuario(usuario._id)
            lista_status = status_dao.listar_status()
            lista_prioridades = prioridade_dao.listar_prioridades()
            
            return render_template('index.html', proxima=proxima, tarefas=lista, tipos=lista_tipo, status_list=lista_status, prioridades=lista_prioridades, usuario=usuario)
        
        except:
            proxima = request.args.get('proxima')
    
            return render_template('landing.html', proxima=proxima)
    
    else:
        
        proxima = request.args.get('proxima')
    
        return render_template('landing.html', proxima=proxima)
       

@app.route('/novo')
def novo():

    return render_template('novo.html')

# Recebe os valores passados via formulário HTML
@app.route('/criar', methods=['POST', ])
def criar():
    try:
        nome = request.form['nome']
        descricao = request.form['descricao']
        tipo_id = request.form['tipo']
        status_id = request.form['status']
        prioridade_id = request.form['prioridade']
        usuario_id = request.form['usuario_id']
        data_prevista = request.form['data_prevista']

        tarefa = Tarefa(nome, descricao, tipo_id, status_id, prioridade_id, None, None, None, usuario_id, data_prevista)
    
        tarefa = tarefa_dao.salvar(tarefa)

    except:

        flash(u"Houve um erro ao criar a tarefa. Tente preencher os campos novamente ou recarregue a página", "msg-ul-bad-solid")

    return redirect('/')


# Função que recebe o id da tarefa desejada e recebe seus respectivos valores do banco de dados

@app.route('/editar_tarefa/<int:id>')
def editar_tarefa(id):
    usuario = usuario_dao.buscar_usuario_por_id(session['usuario_logado'])
    tarefa = tarefa_dao.busca_por_id(id)
    lista_tipo = tipo_dao.listar_tipo_usuario(usuario._id)
    lista_status = status_dao.listar_status()
    lista_prioridade = prioridade_dao.listar_prioridades()
    
    return render_template('/tarefa_edit.html', tarefa=tarefa, tipos=lista_tipo, status_list=lista_status, prioridades=lista_prioridade, usuario=usuario)


# Altera os valores da tarefa desejada, através da função atualizar que é chamada ao editar uma tarefa, a qual já tem seu Id selecionado devido ao HTML de editar

@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    descricao = request.form['descricao']
    tipo_id = request.form['tipo']
    status_id = request.form['status']
    prioridade_id = request.form['prioridade']
    usuario_id = request.form['usuario_id']
    id = request.form['id']

    tarefa = Tarefa(nome, descricao, tipo_id, status_id, prioridade_id, None, None, None, usuario_id, id)

    tarefa_dao.salvar(tarefa)

    return redirect('/')


# Cria uma grande lista com todas as tarefas
@app.route('/lista_de_tarefas')
def lista_de_tarefas():
    lista = tarefa_dao.listar()
    
    return render_template('index.html', tarefas=lista)


# Faz praticamente o mesmo que o "editar", exceto que na há alterações no banco
@app.route('/tarefa_info/<int:id>')
def tarefa_info(id):
    usuario = usuario_dao.buscar_usuario_por_id(session['usuario_logado'])
    lista = tarefa_dao.busca_por_id(id)
    
    return render_template('tarefa_info.html', tarefa=lista, usuario=usuario)


# Remove uma tarefa por seu id
@app.route('/deletar_tarefa/<int:id>')
def deletar_tarefa(id):
    tarefa_dao.deletar(id)
    
    return redirect('/')

# USUARIO

# Adiciona um novo usuário no banco através do formulário HTML
@app.route('/criar_usuario', methods=['POST', ])
def criar_usuario():
    username = request.form['username']
    email = request.form['email']
    senha = request.form['senha']
    
    usuario = Usuario(username, email, senha)
    
    usuario_dao.salvar_usuario(usuario)
    
    return redirect('/')


# Cria uma sessão para o usuário que fez o login corretamente
@app.route('/login')
def login():
    proxima=request.args.get('proxima')
    if proxima == None:
        proxima= ''
    return render_template('index.html', proxima=proxima)


# Verifica se os dados de login estão corretos e se correto,cria uma sessão para o usuário, se não, pede para que o usuário tente fazer login novamente 
@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_email_usu(request.form['email'])
    if usuario:
        if usuario._senha == request.form['senha']:
            session['usuario_logado'] = usuario._id
            flash(usuario._nome + ' logou com sucesso!', 'msg-ul-good')
            return redirect('/')
        
    flash(u'Erro ao logar! Tente novamente.', 'msg-ul-bad')
    
    return  redirect('/')           


# Remove o usuário da sessão
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash(u'Nenhum usuário logado', 'msg-ul-bad')
    
    return redirect('/')


# Acessa o perfil do usuário, retornando estatísticas de seu progresso
@app.route('/perfil/<int:id>')
def perfil(id):
    usuario = usuario_dao.buscar_usuario_por_id(id)
    tarefas_qnt = usuario_dao.conta_tarefas(id)
    tarefas_prontas = usuario_dao.conta_tarefas_prontas(id)
    tarefas_fazendo = usuario_dao.conta_tarefas_fazendo(id)
    tarefas_fazer = usuario_dao.conta_tarefas_fazer(id)
    
    return render_template('profile.html', usuario=usuario, tarefas_qnt=tarefas_qnt, tarefas_prontas=tarefas_prontas, tarefas_fazendo=tarefas_fazendo, tarefas_fazer=tarefas_fazer)

@app.route('/status')
def status():

    return render_template('status.html')


@app.route('/sobre')
def sobre():

    return render_template('sobre.html')


@app.route('/progresso')
def progresso():

    return render_template('progresso.html')


@app.route('/pesquisar/<string:nome>', methods=['POST', ])
def pesquisar():
    nome = request.form['profile-search']

    lista_tarefas = tarefa_dao.busca_por_nome(nome)
    
    return redirect('/lista', tarefas=lista_tarefas)


# -------------------------------- Criar tipo ---------------------------
# Cria um novo tipo através de um formulário HTML
@app.route('/criar_tipo', methods=['POST', ])
def criar_tipo():
    nome = request.form['nome']
    usuario_id = request.form['usuario_id']

    tipo = Tipo(nome, usuario_id)
    
    tipo = tipo_dao.salvar_tipo(tipo)

    return redirect('/')


@app.route('/editar_tipo/<int:id>')
def editar_tipo(id):
    tipo = tipo_dao.busca_por_id(id)
    
    return render_template('/tarefa_edit.html', tipo=tipo)


@app.route('/atualizar_tipo', methods=['POST', ])
def atualizar_tipo():
    nome = request.form['nome']
    usuario_id = request.form['usuario_id']
    id = request.form['id']

    tipo = Tipo(nome, usuario_id, id)

    tipo_dao.salvar_tipo(tipo)

    return redirect('/')


# Deleta um tipo do banco de dados
@app.route('/deletar_tipo/<int:id>')
def deletar_tipo(id):
    tipo_dao.deletar_tipo(id)
    
    return redirect('/')



if __name__ == '__main__':

    app.run(debug=True)
