from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "Restaurante"
app.secret_key = "mysecretkey"

mysql = MySQL(app)

calificacion_maxima = 5

def imprimirErrores(texto, exception):
    print(f"""

<<< [Error] >>>
{texto}: {exception}
<<< [Error] >>>

""")

@app.route("/DBCheck")
def dbCheck():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        return jsonify({"status": "Ok", "message": "Conectado con exito"}), 200
    except MySQLdb.MySQLError as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route("/")
def home():
    try:
        #errores = session.get("errores", "")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Calificaciones WHERE Estado = 1")
        consultarTodo = cursor.fetchall()
        return render_template("registros.html", errores = {}, restaurantes = consultarTodo)
    except Exception as e:
        imprimirErrores("Error al mostrar datos", e)
        return render_template("registros.html", errores = {}, restaurantes = [])
    finally:
        cursor.close()

@app.route("/detalles_restaurante/<int:id>")
def detalles(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Calificaciones WHERE ID = %s", (id,))
        consultarDetalles = cursor.fetchone()
        return render_template("consulta.html", detalles = consultarDetalles)
    except Exception as e:
        imprimirErrores("Error al consultar los detalles", e)
        return redirect(url_for("home"))
    finally:
        cursor.close()

@app.route("/agregar_restaurante", methods = ["POST"])
def agregarRestaurante():
    errores = {}

    restaurante = request.form.get("txtRestaurante", "").strip().title()
    tipo_de_comida = request.form.get("txtTipoDeComida", "").strip().capitalize()
    comentario = request.form.get("txtComentario", "").strip().capitalize()
    calificacion = request.form.get("intCalificacion", "")

    if not restaurante:
        errores["txtRestaurante"] = "Nombre del restaurante obligatorio"
    if not tipo_de_comida:
        errores["txtTipoDeComida"] = "Tipo de comida obligatorio"
    if not calificacion:
        errores["intCalificacion"] = "Calificación obligatoria"
    elif not calificacion.isdigit() or int(calificacion) not in range(0, calificacion_maxima + 1):
        errores["intCalificacion"] = "Calificación fuera de rango"

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO Calificaciones(Restaurante, Tipo_de_comida, Comentario, Calificacion) VALUES(%s, %s, %s, %s)", (restaurante, tipo_de_comida, comentario, calificacion))
            mysql.connection.commit()
            flash("El restaurante se agregó con éxito")
            return redirect(url_for("home"))
        except Exception as e:
            imprimirErrores("Error al insertar datos en la base de datos", e)
            flash("No se pudo agregar el restaurante, inténtelo de nuevo más tarde")
            return redirect(url_for("home"))
        finally:
            cursor.close()
    #session["errores"] = errores
    #return redirect(url_for("home"))
    return render_template("registros.html", errores = errores)

@app.route("/actualizar_restaurante/<int:id>")
def actualizarRestaurante(id):
    try:
        errores = session.get("errores", "")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Calificaciones WHERE ID = %s", (id,))
        consultarDetalles = cursor.fetchone()
        return render_template("actualizarRestaurante.html", errores = errores, detalles = consultarDetalles)
    except Exception as e:
        imprimirErrores("Error al actualizar datos en la base de datos", e)
        return redirect(url_for("detalles", id = id))
    finally:
        cursor.close()

@app.route("/editar_restaurante/<int:id>", methods = ["POST"])
def editarRestaurante(id):
    errores = {}

    restaurante = request.form.get("txtRestaurante", "").strip().title()
    tipo_de_comida = request.form.get("txtTipoDeComida", "").strip().capitalize()
    comentario = request.form.get("txtComentario", "").strip().capitalize()
    calificacion = request.form.get("intCalificacion", "")

    if not restaurante:
        errores["txtRestaurante"] = "Nombre del restaurante obligatorio"
    if not tipo_de_comida:
        errores["txtTipoDeComida"] = "Tipo de comida obligatorio"
    if not calificacion:
        errores["intCalificacion"] = "Calificación obligatoria"
    elif not calificacion.isdigit() or int(calificacion) not in range(0, calificacion_maxima + 1):
        errores["intCalificacion"] = "Calificación fuera de rango"

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE Calificaciones SET Restaurante = %s, Tipo_de_comida = %s, Comentario = %s, Calificacion = %s WHERE ID = %s", (restaurante, tipo_de_comida, comentario, calificacion, id))
            mysql.connection.commit()
            flash("El restaurante se actualizó con éxito")
            return redirect(url_for("home"))
        except Exception as e:
            mysql.connection.rollback()
            imprimirErrores("Error", e)
            flash("No se pudo actualizar el restaurante, inténtelo de nuevo más tarde")
            return redirect(url_for("detalles", id = id))
        finally:
            cursor.close()
    session["errores"] = errores
    return redirect(url_for("actualizarRestaurante", id = id))

@app.route("/eliminar_restaurante/<int:id>")
def eliminar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Calificaciones WHERE ID = %s", (id,))
        consultarDetalles = cursor.fetchone()
        return render_template("confirmarEliminarRestaurante.html", detalles = consultarDetalles)
    except Exception as e:
        imprimirErrores("Error", e)
        return redirect(url_for("detalles", id = id))
    finally:
        cursor.close()

@app.route("/confirmar_eliminar_restaurante/<int:id>", methods = ["POST"])
def confirmarEliminar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Calificaciones SET Estado = 0 WHERE ID = %s;", (id,))
        mysql.connection.commit()
        flash("El album se eliminó de la base de datos")
        return redirect(url_for("home"))
    except Exception as e:
        mysql.connection.rollback()
        imprimirErrores("Error al eliminar el restaurante de la base de datos", e)
        flash("No se pudo eliminar el restaurante, inténtelo de nuevo más tarde")
        return redirect(url_for("detalles", id = id))
    finally:
        cursor.close()

@app.errorhandler(404)
def paginaNoEncontrada(e):
    return "¡Cuidado, error de capa 8!", 404

@app.errorhandler(405)
def error505(e):
    return "¡Revisa el método de envio!", 405

if __name__ == "__main__":
    app.run(port = 3000, debug = True)