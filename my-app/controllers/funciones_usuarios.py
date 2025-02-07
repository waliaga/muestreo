# Python con PostgreSQL
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD


import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio

import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file

# Importar DictCursor para obtener resultados como diccionarios
from psycopg2.extras import DictCursor

# ********************************************************** sección de usuarios **********************************************************
   

# Lista de Usuarios creados
def lista_usuariosBD():
    try:
        with connectionBD() as conexion_PostgreSQLdb:
            with conexion_PostgreSQLdb.cursor(cursor_factory=DictCursor) as cursor:
                querySQL = "SELECT id, name_surname, email_user, created_user FROM users"
                cursor.execute(querySQL)
                usuariosBD = cursor.fetchall()
        return usuariosBD
    except Exception as e:
        print(f"Error en lista_usuariosBD : {e}")
        return []


# Eliminar usuario
def eliminarUsuario(id):
    try:
        with connectionBD() as conexion_PostgreSQLdb:
            with conexion_PostgreSQLdb.cursor(cursor_factory=DictCursor) as cursor:
                querySQL = "DELETE FROM users WHERE id = %s"
                cursor.execute(querySQL, (id,))
                conexion_PostgreSQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario : {e}")
        return []