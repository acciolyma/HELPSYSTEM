# ROTAS DO SITE

from flask import Flask, render_template
from models import db, Pergunta # Importa o banco de dados e o modelo de Pergunta


app = Flask(__name__)

# criar a 1ª página do site
# route -> dominio.com/home     
# função -> o que você quer exibir naquela página
#template 

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db.init_app(app)

# Páginas do site
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/")
def homepage():
    return render_template("homepage.html")

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
