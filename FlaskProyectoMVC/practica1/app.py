from flask import Flask, jsonify
from flask_mysqldb import MySQL
import MySQLdb
from config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    from controllers.albumController import albumBP
    app.register_blueprint(albumBP)
    return app

"""
@app.route("/DBCheck")
def dbCheck():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        return jsonify({"status": "Ok", "message": "Conectado con éxito"}), 200
    except MySQLdb.MySQLError as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.errorhandler(404)
def paginaNoEncontrada(e):
    return "¡Cuidado, error de capa 8!", 404

@app.errorhandler(405)
def error505(e):
    return "¡Revisa el método de envío!", 405

@app.route("/usuario")
@app.route("/usuaria")
def dobleRoute():
    return "Soy el mismo recurso del servidor"
"""

if __name__ == "__main__":
    app = create_app()
    app.run(port=3000, debug=True)
