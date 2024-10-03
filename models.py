from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

# Tabela de Usuários (trabalhadores)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    perguntas = db.relationship('Pergunta', backref='autor', lazy=True)
    respostas = db.relationship('Resposta', backref='autor', lazy=True)

    def __repr__(self):
        return f'Usuario("{self.nome}", Email: "{self.email}")'

# Tabela de Perguntas
class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    respostas = db.relationship('Resposta', backref='pergunta', lazy=True)

    def __repr__(self):
        return f'Pergunta("{self.titulo}", Autor: "{self.autor.nome}")'

# Tabela de Respostas
class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)

    def __repr__(self):
        return f'Resposta(Autor: "{self.autor.nome}", Pergunta ID: {self.pergunta_id})'

# Rota para homepage
@app.route('/')
def homepage():
    return "<h1>Bem-vindo ao Help System!</h1><p>Veja as perguntas disponíveis ou faça login para participar.</p>"

# Rota para visualizar perguntas
@app.route('/perguntas')
def ver_perguntas():
    perguntas = Pergunta.query.all()
    return render_template('perguntas.html', perguntas=perguntas)

# Cria o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
