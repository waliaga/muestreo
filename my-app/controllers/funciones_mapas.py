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

from flask import Flask, jsonify
from conexion.conexionBD import connectionBD
from psycopg2.extras import DictCursor

# ********************************************************** sección de mapas     **********************************************************

from psycopg2.extras import DictCursor

def obtener_parcelas():
    try:
        with connectionBD().cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
                SELECT region, departamento, municipio, sup_parcelas, num_parcelas, densidad, longitud_x, latitud_y, cod_hex, foto_punto
               FROM unodc_parcelas WHERE seleccionado = 1;

            """)
            # FROM parcelas_registro WHERE seleccionado in (2,3) ************** cuando registramos parcelas
            # FROM unodc_parcelas WHERE seleccionado = 1 LIMIT 100; ************** cuando seleccionamos parcelas
            
            parcelas = cursor.fetchall()
            return parcelas
    except Exception as e:
        print(f"Error al obtener parcelas: {e}")
        return []

def obtener_superficies_por_municipio():
    try:
        with connectionBD().cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
                SELECT municipio, SUM(sup_muestra) AS suma 
                FROM unodc_parcelas 
                GROUP BY cod_mun, municipio 
                ORDER BY cod_mun;
            """)
            superficies = cursor.fetchall()
            print("Superficies por municipio:", superficies)  # Agregar impresión para depuración
            return superficies
    except Exception as e:
        print(f"Error al obtener superficies por municipio: {e}")
        return []

def obtener_densidades():
    try:
        with connectionBD().cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
                SELECT densidad, COUNT(id) AS sorteados 
                FROM unodc_parcelas 
                WHERE seleccionado = 1 
                GROUP BY densidad 
                ORDER BY densidad;
            """)
            densidades = cursor.fetchall()
            return densidades
    except Exception as e:
        print(f"Error al obtener densidades: {e}")
        return []
    