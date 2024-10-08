from flask import Flask, render_template, request, redirect, url_for, flash, session
from bancodedados import db, Usuario, Pergunta, Resposta
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SECRET_KEY'] = 'chavesecreta'
db.init_app(app)

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota para página de cadastro
@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)

        # Verifica se já existe um usuário com o mesmo e-mail
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Email já cadastrado. Tente outro.', 'error')
            return redirect(url_for('cadastro'))

        # Cria novo usuário
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('homepage'))

    return render_template("cadastro.html")

# Rota para página inicial (homepage)
@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verifica se o usuário existe e se a senha está correta
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario or not check_password_hash(usuario.senha, senha):
            flash('Email ou senha incorretos', 'error')
            return redirect(url_for('homepage'))

        # Salva o ID do usuário na sessão
        session['user_id'] = usuario.id
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('menu'))

    return render_template("login.html")

# Rota para adicionar pergunta
@app.route("/pergunta", methods=['GET', 'POST'])
def pergunta():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']

        if 'user_id' not in session:
            flash('Você precisa estar logado para adicionar uma pergunta.', 'error')
            return redirect(url_for('menu'))

        autor_id = session.get('user_id')

        try:
            nova_pergunta = Pergunta(titulo=titulo, conteudo=conteudo, data_criacao=datetime.utcnow(), autor_id=autor_id)
            db.session.add(nova_pergunta)
            db.session.commit()
            flash('Pergunta adicionada com sucesso!', 'success')
        except Exception as e:
            app.logger.error(f"Erro ao adicionar pergunta: {e}")
            flash('Ocorreu um erro ao adicionar a pergunta. Por favor, tente novamente mais tarde.', 'error')

        return redirect(url_for('menu'))  # Redireciona para o menu após adicionar a pergunta

    return render_template("pergunta.html")

# Rota para o menu que lista todas as perguntas
@app.route("/menu")
def menu():
    perguntas = Pergunta.query.order_by(Pergunta.data_criacao.desc()).all()  # Ordena as perguntas da mais recente para a mais antiga
    for pergunta in perguntas:
        pergunta.respostas = Resposta.query.filter_by(pergunta_id=pergunta.id).all()  # Obtém respostas para a pergunta

    return render_template("homepage.html", perguntas=perguntas)  # Passa as perguntas para o template

# Rota para adicionar uma resposta
@app.route('/responder_pergunta/<int:pergunta_id>', methods=['POST'])
def adicionar_resposta(pergunta_id):
    if 'user_id' not in session:
        flash('Você precisa estar logado para responder.', 'error')
        return redirect(url_for('menu'))

    conteudo = request.form['conteudo']
    autor_id = session['user_id']

    # Adiciona uma nova resposta à pergunta especificada
    nova_resposta = Resposta(conteudo=conteudo, autor_id=autor_id, pergunta_id=pergunta_id)
    db.session.add(nova_resposta)
    db.session.commit()
    flash('Resposta adicionada com sucesso!', 'success')

    return redirect(url_for('menu'))

# Rota para excluir perguntas (somente o autor pode excluir)
@app.route('/excluir_pergunta/<int:pergunta_id>', methods=['POST'])
def excluir_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    autor_id = session.get('user_id')

    if pergunta.autor_id != autor_id:
        flash('Você não tem permissão para excluir esta pergunta.', 'error')
        return redirect(url_for('menu'))

    # Excluir todas as respostas associadas à pergunta
    for resposta in pergunta.respostas:
        db.session.delete(resposta)

    # Agora, exclua a pergunta
    db.session.delete(pergunta)
    db.session.commit()
    flash('Pergunta excluída com sucesso!', 'success')
    return redirect(url_for('menu'))

@app.route('/excluir_resposta/<int:resposta_id>', methods=['POST'])
def excluir_resposta(resposta_id):
    resposta = Resposta.query.get_or_404(resposta_id)
    autor_id = session.get('user_id')

    if resposta.autor_id != autor_id:
        flash('Você não tem permissão para excluir esta resposta.', 'error')
        return redirect(url_for('menu'))

    db.session.delete(resposta)
    db.session.commit()
    flash('Resposta excluída com sucesso!', 'success')
    return redirect(url_for('menu'))

# Rota para adicionar pergunta (diretamente do menu)
@app.route("/adicionar_pergunta", methods=['POST'])
def adicionar_pergunta():
    if 'user_id' not in session:
        flash('Você precisa estar logado para adicionar uma pergunta.', 'error')
        return redirect(url_for('menu'))

    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    autor_id = session['user_id']

    nova_pergunta = Pergunta(titulo=titulo, conteudo=conteudo, data_criacao=datetime.utcnow(), autor_id=autor_id)
    db.session.add(nova_pergunta)
    db.session.commit()
    flash('Pergunta adicionada com sucesso!', 'success')

    return redirect(url_for('menu'))  # Redireciona para o menu após adicionar a pergunta

# Inicia o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
