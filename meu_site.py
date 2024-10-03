from flask import Flask, render_template

app = Flask(__name__)

# criar a 1ª página do site
# route -> dominio.com/home     
# função -> o que você quer exibir naquela página
#template 

@app.route("/")  #app é o nome do site
def homepage():
    return render_template("homepage.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/usuarios/<nome_usuario>")   #criação de página personalizada
def usuarios(nome_usuario):
    return render_template("usuarios.html", nome_usuario=nome_usuario)



# colcar o site no ar:

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

    #servidor do heroku
    