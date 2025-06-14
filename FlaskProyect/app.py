from flask import Flask, jsonify
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "dbflask"
# app.config["MYSQL_PORT"] = 3306 // Usar sólo si se cambió el puerto predeterminado de MySQL

mysql = MySQL(app)

# Ruta para probar la conexión a MySQL
@app.route("/DBCheck")
def dbCheck():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        return jsonify({"status": "Ok", "message": "Conectado con exito"}), 200
    except MySQLdb.MySQLError as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

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