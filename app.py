from flask import Flask, render_template, request, redirect, session, flash, jsonify

from dao import StatusDao, TarefaDao, TipoDao, UsuarioDao, PrioridadeDao

from werkzeug.security import check_password_hash, generate_password_hash

from models import Tarefa, Usuario, Tipo

from functools import wraps

import sqlite3

app = Flask(__name__)
app.secret_key = 'ENGII'

db = sqlite3.connect('database.db', check_same_thread=False)

# dao

tarefa_dao = TarefaDao(db)
usuario_dao = UsuarioDao(db)
tipo_dao = TipoDao(db)
status_dao = StatusDao(db)
prioridade_dao = PrioridadeDao(db)

# Login required function ------------------------------------------------

@app.before_first_request
def before_request_fkey():

    db.execute("PRAGMA foreign_keys=ON")


@app.errorhandler(404)
def page_not_found(e):

    error_img = '../static/imgs/404.gif'
    error_number = '404'
    error_description = 'Page not found.'

    return render_template('error.html', error_img=error_img, error_number=error_number, error_description=error_description), 404


@app.errorhandler(500)
def internal_server_error(e):
    
    error_img = '../static/imgs/500.gif'
    error_number = '500'
    error_description = 'Internal server error.'

    return render_template('error.html', error_img=error_img, error_number=error_number, error_description=error_description), 500


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('usuario_logado' not in session) or session['usuario_logado'] == None:

            flash(u"Você necessita de login para acessar essa página.", "msg-ul-bad")

            return redirect('/')
            
        return f(*args, **kwargs)    
        
    return wrap

# --------------------------------------------------------------------------


@app.route('/')
def index():
    if session == None or session == "":

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
        
        except Exception:

            proxima = request.args.get('proxima')
    
            return render_template('landing.html', proxima=proxima)

    else:

        proxima = request.args.get('proxima')

        return render_template('landing.html', proxima=proxima)
       

@app.route('/novo')
@login_required
def novo():

    return render_template('novo.html')

# Recebe os valores passados via formulário HTML
@app.route('/criar', methods=['POST',])
@login_required
def criar():
    try:
        nome = request.form['nome']
        descricao = request.form['descricao']
        tipo_id = request.form['tipo']
        status_id = request.form['status']
        prioridade_id = request.form['prioridade']
        usuario_id = request.form['usuario_id']
        data_prevista = request.form['data_prevista']

        tarefa = Tarefa(nome, descricao, tipo_id, status_id, prioridade_id, None, None, None, usuario_id, data_prevista, None)

        tarefa = tarefa_dao.salvar(tarefa)

        return redirect('/')
    
    except Exception:

        flash(u'Um erro inesperado ocorreu, tente criar uma tarefa novamente mais tarde.', 'msg-ul-bad-solid')

        return redirect('/')


# Função que recebe o id da tarefa desejada e recebe seus respectivos valores do banco de dados
@app.route('/editar_tarefa/<int:id>')
@login_required
def editar_tarefa(id):

    usuario = usuario_dao.buscar_usuario_por_id(session['usuario_logado'])
    tarefa = tarefa_dao.busca_por_id(id)
    lista_tipo = tipo_dao.listar_tipos_do_usuario(session['usuario_logado'])
    lista_status = status_dao.listar_status()
    lista_prioridade = prioridade_dao.listar_prioridades()
    
    return render_template('/tarefa_edit.html', tarefa=tarefa, tipos=lista_tipo, status_list=lista_status, prioridades=lista_prioridade, usuario=usuario)


# Altera os valores da tarefa desejada, através da função atualizar que é chamada ao editar uma tarefa, a qual já tem seu Id selecionado devido ao HTML de editar
@app.route('/atualizar', methods=['POST', ])
@login_required
def atualizar():

    try:
    
        nome = request.form['nome']
        descricao = request.form['descricao']
        tipo_id = request.form['tipo']
        status_id = request.form['status']
        prioridade_id = request.form['prioridade']
        usuario_id = request.form['usuario_id']
        data_criacao = request.form['data_criacao']
        data_prevista = request.form['data_prevista']
        id = request.form['id']

        tarefa = Tarefa(nome, descricao, tipo_id, status_id, prioridade_id, None, None, None, usuario_id, data_prevista, data_criacao, data_prevista, id)

        tarefa_dao.salvar(tarefa)

        flash(u'Tarefa atualizada com sucesso! :)', "msg-ul-good")

    except Exception:

        flash(u'Erro ao atualizar a tarefa. Tente novamente', 'msg-ul-bad')

    return redirect(f'/tarefa_info/{id}')


# Cria uma grande lista com todas as tarefas

@app.route('/lista_de_tarefas')
def lista_de_tarefas():
    lista = tarefa_dao.listar()
    
    return render_template('index.html', tarefas=lista)


# Faz praticamente o mesmo que o "editar", exceto que na há alterações no banco

@app.route('/tarefa_info/<int:id>')
@login_required
def tarefa_info(id):
    usuario = usuario_dao.buscar_usuario_por_id(session['usuario_logado'])
    lista = tarefa_dao.busca_por_id(id)
    lista_tipo = tipo_dao.listar_tipo_usuario(usuario._id)
    lista_status = status_dao.listar_status()
    lista_prioridade = prioridade_dao.listar_prioridades()
    
    return render_template('tarefa_info.html', tarefa=lista, usuario=usuario, tipos=lista_tipo, status_list=lista_status, prioridades=lista_prioridade)


# Remove uma tarefa por seu id

@app.route('/deletar_tarefa/<int:id>')
@login_required
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

        if usuario._senha == request.form['senha'] and usuario._email == request.form['email']:
            
            session['usuario_logado'] = usuario._id

            flash(usuario._nome + ' logou com sucesso!', 'msg-ul-good')

            return redirect('/')
        
        else:

            flash(u'Erro ao fazer login. Analise os dados e tente novamente', 'msg-ul-bad')

        return  redirect('/')           


# Remove o usuário da sessão
@app.route('/logout')
@login_required
def logout():

    session['usuario_logado'] = None

    flash(u'Nenhum usuário logado', 'msg-ul-bad')
    
    return redirect('/')


# Acessa o perfil do usuário, retornando estatísticas de seu progresso
@app.route('/perfil/<int:id>')
@login_required
def perfil(id):

    usuario = usuario_dao.buscar_usuario_por_id(id)
    tarefas_qnt = usuario_dao.conta_tarefas(id)
    tarefas_prontas = usuario_dao.conta_tarefas_prontas(id)
    tarefas_fazendo = usuario_dao.conta_tarefas_fazendo(id)
    tarefas_fazer = usuario_dao.conta_tarefas_fazer(id)
    tipos = tipo_dao.listar_tipos_do_usuario(id)
    
    return render_template('profile.html', usuario=usuario, tarefas_qnt=tarefas_qnt, tarefas_prontas=tarefas_prontas, tarefas_fazendo=tarefas_fazendo, tarefas_fazer=tarefas_fazer, tipos=tipos)


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
@login_required
def criar_tipo():
    
    nome = request.form['nome']

    usuario_id = request.form['usuario_id']

    tipo = Tipo(nome, usuario_id)
    
    tipo = tipo_dao.salvar_tipo(tipo)

    return redirect('/')


@app.route('/editar_tipo/<int:id>')
@login_required
def editar_tipo(id):

    usuario = usuario_dao.buscar_usuario_por_id(session['usuario_logado'])

    tipo = tipo_dao.busca_por_id(id)
    
    return render_template('/tipo.html', tipo=tipo, usuario=usuario)


@app.route('/atualizar_tipo', methods=['POST', ])
@login_required
def atualizar_tipo():

    nome = request.form['nome']

    usuario_id = request.form['usuario_id']
    
    id = request.form['id']

    tipo = Tipo(nome, usuario_id, id)

    tipo_dao.salvar_tipo(tipo)

    return redirect('/')


# Deleta um tipo do banco de dados
@app.route('/deletar_tipo/<int:id>')
@login_required
def deletar_tipo(id):
    tipo_dao.deletar_tipo(id)
    
    return redirect('/')



if __name__ == '__main__':

    app.run(debug=True)