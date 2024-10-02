from flask import Flask

app = Flask(__name__)

# criar a 1ª página do site
# route -> dominio.com/home      https://glorious-goldfish-55vvpj47rx7hvg6q-5000.app.github.dev/
# função -> o que você quer exibir naquela página

@app.route("/")  #app é o nome do site
def homepage():
    return "Esse é o meu primeito site"


# colcar o site no ar
app.run()
