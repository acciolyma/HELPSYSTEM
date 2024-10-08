from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

# Importa os modelos
from bancodedados import Usuario, Pergunta, Resposta, Comentario

with app.app_context():
    # Deletar todos os dados das tabelas
    db.session.query(Comentario).delete()
    db.session.query(Resposta).delete()
    db.session.query(Pergunta).delete()
    db.session.query(Usuario).delete()
    db.session.commit()

print("Todos os dados foram apagados com sucesso!")
