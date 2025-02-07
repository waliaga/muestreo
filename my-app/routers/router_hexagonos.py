from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_hexagonos import *
 

# ********************************************************** sección de hexagonos **********************************************************
PATH_URL = "public/hexagonos"

# Registrar GET de hexagonos
@app.route('/registrar-hexagono', methods=['GET'])
def viewFormHexagono():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_hexagono.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Registrar POST de hexagonos
@app.route('/form-registrar-hexagono', methods=['POST'])
def formHexagono():
    if 'conectado' in session:
        if 'foto_hexagono' in request.files:
            foto_perfil = request.files['foto_hexagono']
            resultado = procesar_form_hexagono(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_hexagonos'))
            else:
                flash('El hexagono NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_hexagono.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Lista de hexagonos
@app.route('/lista-de-hexagonos', methods=['GET'])
def lista_hexagonos():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_hexagonos.html', hexagonos=sql_lista_hexagonosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# detalles de hexagonos
@app.route("/detalles-hexagono/", methods=['GET'])
@app.route("/detalles-hexagono/<int:idhexagono>", methods=['GET'])
def detalleHexagono(idhexagono=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idhexagono es None o no está presente en la URL
        if idhexagono is None:
            return redirect(url_for('inicio'))
        else:
            detalle_hexagono = sql_detalles_hexagonosBD(idhexagono) or []
            return render_template(f'{PATH_URL}/detalles_hexagono.html', detalle_hexagono=detalle_hexagono)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de hexagonos
@app.route("/buscando-hexagono", methods=['POST'])
def viewBuscarHexagonoBD():
    resultadoBusqueda = buscarHexagonoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_hexagono.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Editar de hexagonos
@app.route("/editar-hexagono/<int:id>", methods=['GET'])
def viewEditarHexagono(id):
    if 'conectado' in session:
        respuestaHexagono = buscarHexagonoUnico(id)
        if respuestaHexagono:
            return render_template(f'{PATH_URL}/form_hexagono_update.html', respuestaHexagono=respuestaHexagono)
        else:
            flash('El hexagono no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de hexagono
@app.route('/actualizar-hexagono', methods=['POST'])
def actualizarHexagono():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_hexagonos'))

# Reporte Exportar a Excel 
@app.route("/descargar-informe-hexagonos/", methods=['GET'])
def reporteBDhex():
    if 'conectado' in session:
        return generarReporteExcelxhex()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
# Generar muestras aleatorias
# Ruta para generar muestras aleatorias
@app.route("/generar-muestras-aleatorias/", methods=['POST'])
def generarMuestrasAleatoriasRoute():
    if 'conectado' in session:  # Verifica si el usuario está conectado
        total_seleccionados = generar_muestras_aleatorias()  # Llama a la función del controlador
        if total_seleccionados is not False:  # Si no hay errores
            flash(f'Se seleccionaron {total_seleccionados} hexágonos correctamente.', 'success')  # Mensaje de éxito
        else:
            flash('Ocurrió un error al generar las muestras.', 'error')  # Mensaje de error
        return redirect(url_for('inicio'))  # Redirecciona a la página de inicio
    else:
        flash('Primero debes iniciar sesión.', 'error')  # Mensaje de error si no está conectado
        return redirect(url_for('inicio'))  # Redirecciona a la página de inicio


