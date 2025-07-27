from flask import Blueprint, jsonify
from flask_mysqldb import MySQLdb
from app import mysql

databaseBP = Blueprint("database", __name__)

@databaseBP.route("/DBCheck")
def dbCheck():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        return jsonify({"status": "Ok", "message": "Conectado correctamente"}), 200
    except MySQLdb.MySQLError as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@databaseBP.errorhandler(404)
def paginaNoEncontrada(e):
    return "¡Cuidado, error de capa 8!", 404

@databaseBP.errorhandler(405)
def error505(e):
    return "¡Revisa el método de envío!", 405