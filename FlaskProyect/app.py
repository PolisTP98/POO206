from flask import Flask

app = Flask(__name__)

# Ruta simple
@app.route("/")
def home():
    return "¡Hola mundo Flask!"

# Ruta con parámetros
@app.route("/saludar/<nombre>")
def saludar(nombre):
    return f"¡Hola {nombre}!"

# Ruta try - catch
@app.errorhandler(404)
def paginaNoEncontrada(e):
    return "¡Cuidado, error de capa 8!", 404

# Ruta doble
@app.route("/usuario")
@app.route("/usuaria")
def dobleRoute():
    return "Soy el mismo recurso del servidor"

# Ruta POST
@app.route("/formulario", methods = ["POST"])
def formulario():
    return "Soy un formulario"

if __name__ == "__main__":
    app.run(port = 3000, debug = True)