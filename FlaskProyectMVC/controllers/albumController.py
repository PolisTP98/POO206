from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.albumModel import *

albumsBP = Blueprint("albums", __name__)
minimum_year, maximum_year = 1800, 2100

# Ruta de inicio (consultar todos los álbumes de la BD)
@albumsBP.route("/")
def inicio():
    try:
        albums = getAll()
        session["html_title"] = "Álbumes"
        return render_template("formulario.html", errores = {}, albums = albums)
    except Exception as e:
        print(f"¡Error!, {e}")
        return render_template("formulario.html", errores = {}, albums = {})
    
# Ruta para guardar un nuevo álbum
@albumsBP.route("/guardarAlbum", methods = ["POST"])
def guardarAlbum():
    errores = {}

    titulo_album = request.form.get("txtTitulo", "").strip()
    artista_album = request.form.get("txtArtista", "").strip()
    lanzamiento_album = request.form.get("txtYear", "").strip()

    if not titulo_album:
        errores["txtTitulo"] = "Nombre del álbum obligatorio"
    if not artista_album:
        errores["txtArtista"] = "Nombre del artista obligatorio"
    if not lanzamiento_album:
        errores["txtYear"] = "Año de lanzamiento obligatorio"
    elif not lanzamiento_album.isdigit() or int(lanzamiento_album) not in range(minimum_year, maximum_year + 1):
        errores["txtYear"] = "Año de lanzamiento inválido"
    
    if errores:
        return render_template("formulario.html", errores = errores, albums = getAll())
    
    try:
        insertAlbum(titulo_album, artista_album, lanzamiento_album)
        flash("¡Álbum agregado exitosamente!")
    except Exception as e:
        print(f"¡Error!, {e}")
        flash("Error al guardar el álbum")
    finally:
        return redirect(url_for("albums.inicio"))
    
# Ruta para ver los detalles de un álbum
@albumsBP.route("/detalleAlbum/<int:id_album>")
def detalleAlbum(id_album):
    try:
        album = getByID(id_album)
        session["html_title"] = f"Detalles de {album[1]}"
        return render_template("consulta.html", album = album)
    except Exception as e:
        print(f"¡Error!, {e}")
        flash("Error al consultar el álbum")
        return redirect(url_for("albums.inicio"))
    
# Ruta para editar un álbum (mostrar formulario)
@albumsBP.route("/editarAlbum/<int:id_album>")
def editarAlbum(id_album):
    try:
        errores = session.get("errores", "")
        album = getByID(id_album)
        session["html_title"] = f"Actualizar {album[1]}"
        return render_template("actualizarAlbum.html", errores = errores, album = album)
    except Exception as e:
        print(f"¡Error!, {e}")
        flash("Error al consultar el álbum a editar")
        return redirect(url_for("albums.inicio"))
    
# Ruta para actualizar un álbum
@albumsBP.route("/actualizarAlbum/<int:id_album>")
def actualizarAlbum(id_album):
    errores = {}

    titulo_album = request.form.get("txtTitulo", "").strip()
    artista_album = request.form.get("txtArtista", "").strip()
    lanzamiento_album = request.form.get("txtYear", "").strip()

    if not titulo_album:
        errores["txtTitulo"] = "Nombre del álbum obligatorio"
    if not artista_album:
        errores["txtArtista"] = "Nombe del artista obligatorio"
    if not lanzamiento_album:
        errores["txtYear"] = "Año de lanzamiento obligatorio"
    elif not lanzamiento_album.isdigit() or int(lanzamiento_album) not in range(minimum_year, maximum_year + 1):
        errores["txtYear"] = "Año de lanzamiento inválido"
    
    if errores:
        session["errores"] = errores
        return redirect(url_for("editarAlbum", id_album = id_album))
    
    try:
        updateAlbum(id_album, titulo_album, artista_album, lanzamiento_album)
        flash("¡Álbum actualizado exitosamente!")
    except Exception as e:
        print(f"¡Error!, {e}")
        flash("Error al actualizar el álbum")
    finally:
        return redirect(url_for("albums.inicio"))
    
# Ruta para confirmar la eliminación de un álbum
@albumsBP.route("/confirmarEliminarAlbum/<int:id_album>")
def confirmarEliminarAlbum(id_album):
    try:
        album = getByID(id_album)
        session["html_title"] = f"Eliminar {album[1]}"
        return render_template("confirmDelete.html", album = album)
    except Exception as e:
        print(f"¡Error!, {e}")
        flash("Error al consultar el álbum a eliminar")
        return redirect(url_for("albums.inicio"))
    
# Ruta para eliminar un álbum (soft delete)
@albumsBP.route("/eliminarAlbum/<int:id_album>")
def eliminarAlbum(id_album):
    try:
        softDeleteAlbum(id_album)
        flash("¡Álbum eliminado exitosamente!")
    except Exception as e:
        print(f"¡Error!, {e}")
        flash("Error al eliminar el álbum")
    finally:
        return redirect(url_for("albums.inicio"))