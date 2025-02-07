# Python con PostgreSQL
from app import app
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session

# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importar funciones para obtener datos
from controllers.funciones_mapas import obtener_parcelas, obtener_superficies_por_municipio, obtener_densidades

# ********************************************************** Sección de mapas **********************************************************

@app.route('/parcelas')
def obtener_parcelas_ruta():
    """
    Ruta para obtener los datos de las parcelas en formato JSON.
    Transforma los arreglos en objetos JSON con claves descriptivas.
    """
    # Obtener los datos de las parcelas desde la base de datos
    parcelas = obtener_parcelas()
    
    # Transformar arreglos en objetos JSON
    parcelas_transformadas = []
    for parcela in parcelas:
        parcela_dict = {
            "region": parcela[0],
            "departamento": parcela[1],
            "municipio": parcela[2],
            "sup_parcelas": parcela[3],
            "num_parcelas": parcela[4],
            "densidad": parcela[5],
            "longitud_x": parcela[6],
            "latitud_y": parcela[7],
            "cod_hex": parcela[8],
            "foto_punto": parcela[9]
        }
        parcelas_transformadas.append(parcela_dict)
    
    # Devolver los datos en formato JSON
    return jsonify(parcelas_transformadas)

# ... (rest of your code)


@app.route('/mi-mapa', methods=['GET'])
def mapa():
    if 'conectado' in session:
        # Obtener datos para el dashboard
        superficies_municipio = obtener_superficies_por_municipio()
        densidades = obtener_densidades()

        # Preparar datos para Chart.js
        surface_labels = [row[0] for row in superficies_municipio]  # Nombres de municipios
        surface_data = [float(row[1]) for row in superficies_municipio]  # Superficies

        density_labels = [str(row[0]) for row in densidades]  # Densidades
        density_data = [int(row[1]) for row in densidades]  # Conteos

        # Pasar los datos al template
        return render_template('public/mapa/mapa.html', 
                              superficies_municipio=superficies_municipio, 
                              densidades=densidades,
                              surface_labels=surface_labels,
                              surface_data=surface_data,
                              density_labels=density_labels,
                              density_data=density_data)
    else:
        return redirect(url_for('inicio'))