from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Usuario, Pergunta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SECRET_KEY'] = 'chavesecreta'
db.init_app(app)

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

        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template("homepage.html")


# Rota para pergunta
@app.route('/pergunta', methods=['POST'])
def adicionar_pergunta():
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    autor_id = session.get('user_id')  # Supondo que você armazena o ID do usuário na sessão #OLHEM ISSO AQUI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    nova_pergunta = Pergunta(titulo=titulo, conteudo=conteudo, data_criacao=datetime.utcnow(), autor_id=autor_id)
    db.session.add(nova_pergunta)
    db.session.commit()

    return redirect('/dashboard')  # Redireciona para o dashboard após salvar

@app.route('/login', methods=['POST'])
def login():
    # Lógica de autenticação...
    session['user_id'] = usuario.id  # Armazenando o ID do usuário na sessão
    return redirect('/dashboard')


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/pergunta")
def pergunta():
    perguntas = Pergunta.query.all()  # Exibe todas as perguntas
    return render_template("pergunta.html", perguntas=perguntas)

# Inicia o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
