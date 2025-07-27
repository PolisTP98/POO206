from app import mysql

# Método para obtener todos los álbumes activos
def getAll():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM TBAlbum WHERE Estado = 1")
    resultado = cursor.fetchall()
    return resultado

# Método que obtiene un álbum específico según su ID
def getByID(id_album):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM TBAlbum WHERE ID_registro = %s", (id_album,))
    resultado = cursor.fetchone()
    return resultado

# Método para insertar un nuevo álbum
def insertAlbum(titulo_album, artista_album, lanzamiento_album):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO TBAlbum(Nombre_album, Artista_album, Year_lanzamiento) VALUES (%s, %s, %s)", (titulo_album, artista_album, lanzamiento_album))
    mysql.connection.commit()
    cursor.close()

# Método para actualizar un álbum
def updateAlbum(id_album, titulo_album, artista_album, lanzamiento_album):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE TBAlbum SET Nombre_album = %s, Artista_album = %s, Year_lanzamiento = %s WHERE ID_registro = %s)", (titulo_album, artista_album, lanzamiento_album, id_album))
    mysql.connection.commit()
    cursor.close()

# Método para eliminar lógicamente un álbum (soft delete)
def softDeleteAlbum(id_album):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE TBAlbum SET Estado = 0 WHERE ID_registro = %s", (id_album,))
    mysql.connection.commit()
    cursor.close()