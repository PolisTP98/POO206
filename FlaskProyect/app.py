from flask import Flask, jsonify, render_template, request, url_for, flash, redirect, session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123456"
app.config["MYSQL_DB"] = "dbflask"
app.secret_key = "mysecretkey"
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
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM TBAlbum WHERE Estado = 1")
        consultarTodo = cursor.fetchall()
        return render_template("formulario.html", errores = {}, albums = consultarTodo)
    except Exception as e:
        print(f"Error al consultar todo: {e}")
        return render_template("formulario.html", errores = {}, albums = [])
    finally:
        cursor.close()

@app.route("/detalles/<int:id_album>")
def detalles(id_album):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM TBAlbum WHERE ID_registro = %s", (id_album,))
        consultarDetalles = cursor.fetchone()
        return render_template("consulta.html", errores = {}, detalles = consultarDetalles)
    except Exception as e:
        print(f"Error al consultar los detalles: {e}")
        return redirect(url_for("home"))
    finally:
        cursor.close()

@app.route("/EliminarAlbum/<int:id_album>")
def eliminar(id_album):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM TBAlbum WHERE ID_registro = %s", (id_album,))
        consultarDetalles = cursor.fetchone()
        return render_template("confirmDelete.html", detalles = consultarDetalles)
    except Exception as e:
        print(f"Error al consultar los detalles: {e}")
        return redirect(url_for("detalles", id_album = id_album))
    finally:
        cursor.close()

@app.route("/ConfirmarEliminarAlbum/<int:id_album>", methods = ["POST"])
def confirmarEliminar(id_album):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE TBAlbum SET Estado = 0 WHERE ID_registro = %s;", (id_album,))
        mysql.connection.commit()
        flash("El album se eliminó de la base de datos")
        return redirect(url_for("home"))
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Algo falló: {e}")
        return redirect(url_for("home"))
    finally:
        cursor.close()


@app.route("/consulta")
def consulta():
    return render_template("consulta.html")

# Ruta con parámetros
@app.route("/saludar/<nombre>")
def saludar(nombre):
    return f"¡Hola {nombre}!"

# Ruta try - catch
@app.errorhandler(404)
def paginaNoEncontrada(e):
    return "¡Cuidado, error de capa 8!", 404

@app.errorhandler(405)
def error505(e):
    return "¡Revisa el método de envio!", 405

# Ruta doble
@app.route("/usuario")
@app.route("/usuaria")
def dobleRoute():
    return "Soy el mismo recurso del servidor"

# Ruta POST
@app.route("/formulario", methods = ["POST"])
def formulario():
    return "Soy un formulario"

# Ruta para insert
@app.route("/guardarAlbum", methods = ["POST"])
def guardar():

    # Lista de errores
    errores = {}

    # Obtener los datos a guardar
    titulo = request.form.get("txtTitulo", "").strip()
    artista = request.form.get("txtArtista", "").strip()
    year = request.form.get("txtYear", "").strip()

    if not titulo:
        errores["txtTitulo"] = "Nombre del álbum obligatorio"
    if not artista:
        errores["txtArtista"] = "Artista obligatorio"
    if not year:
        errores["txtYear"] = "Año de publicación obligatorio"
    elif not year.isdigit() or int(year) not in range(1800, 2101):
        errores["txtYear"] = "Ingresa un año válido"

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO TBAlbum(Nombre_album, Nombre_artista, Year_lanzamiento) VALUES (%s, %s, %s);", (titulo, artista, year))
            mysql.connection.commit()
            flash("El album se guardó en la base de datos")
            return redirect(url_for("home"))
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Algo falló: {e}")
            return redirect(url_for("home"))
        finally:
            cursor.close()

    return render_template("formulario.html", err = errores)

@app.route("/actualizar/<int:id_album>")
def actualizar(id_album):
    try:
        errores = session.get("errores", "")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM TBAlbum WHERE ID_registro = %s", (id_album,))
        consultarDetalles = cursor.fetchone()
        return render_template("actualizarAlbum.html", err = errores, detalles = consultarDetalles)
    except Exception as e:
        print(f"Error al consultar los detalles: {e}")
        return redirect(url_for("detalles", id_album = id_album))
    finally:
        cursor.close()


@app.route("/actualizarAlbum/<int:id_album>", methods = ["POST"])
def guardarCambios(id_album):

    # Lista de errores
    errores = {}

    # Obtener los datos a guardar
    titulo = request.form.get("txtTitulo", "").strip()
    artista = request.form.get("txtArtista", "").strip()
    year = request.form.get("txtYear", "").strip()

    if not titulo:
        errores["txtTitulo"] = "Nombre del álbum obligatorio"
    if not artista:
        errores["txtArtista"] = "Artista obligatorio"
    if not year:
        errores["txtYear"] = "Año de publicación obligatorio"
    elif not year.isdigit() or int(year) not in range(1800, 2101):
        errores["txtYear"] = "Ingresa un año válido"

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE TBAlbum SET Nombre_album = %s, Nombre_artista = %s, Year_lanzamiento = %s WHERE ID_registro = %s;", (titulo, artista, year, id_album))
            mysql.connection.commit()
            flash("El album se actualizó en la base de datos")
            return redirect(url_for("home"))
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Algo falló: {e}")
            return redirect(url_for("home"))
        finally:
            cursor.close()

    session["errores"] = errores
    return redirect(url_for("actualizar", id_album = id_album))

if __name__ == "__main__":
    app.run(port = 3000, debug = True)