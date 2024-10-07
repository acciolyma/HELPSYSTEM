# CONFIGURAÇÃO BANCO DE DADOS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabela de Usuários (trabalhadores)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    perguntas = db.relationship('Pergunta', backref='autor', lazy=True)
    respostas = db.relationship('Resposta', backref='autor', lazy=True)
    comentarios = db.relationship('Comentario', backref='autor', lazy=True)  # Relacionamento com Comentarios

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
    comentarios = db.relationship('Comentario', backref='resposta', lazy=True)  # Relacionamento com Comentarios

    def __repr__(self):
        return f'Resposta(Autor: "{self.autor.nome}", Pergunta ID: {self.pergunta_id})'

# Tabela de Comentários
class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    resposta_id = db.Column(db.Integer, db.ForeignKey('resposta.id'), nullable=False)

    def __repr__(self):
        return f'Comentario(Autor: "{self.autor.nome}", Resposta ID: {self.resposta_id})'
