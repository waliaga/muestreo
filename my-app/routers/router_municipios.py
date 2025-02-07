from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_municipios import *
  

# ********************************************************** sección de municipios **********************************************************
PATH_URL = "public/municipios"

@app.route('/registrar-municipio', methods=['GET'])
def viewFormMunicipio():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_municipio.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-municipio', methods=['POST'])
def formMunicipio():
    if 'conectado' in session:
        if 'foto_municipio' in request.files:
            foto_perfil = request.files['foto_municipio']
            resultado = procesar_form_municipio(request.form, foto_perfil)
            if resultado:
                return redirect(url_for('lista_municipios'))
            else:
                flash('El municipio NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_municipio.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-municipios', methods=['GET'])
def lista_municipios():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_municipios.html', municipios=sql_lista_municipiosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-municipio/", methods=['GET'])
@app.route("/detalles-municipio/<int:idMunicipio>", methods=['GET'])
def detalleMunicipio(idMunicipio=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idMunicipio es None o no está presente en la URL
        if idMunicipio is None:
            return redirect(url_for('inicio'))
        else:
            detalle_municipio = sql_detalles_municipiosBD(idMunicipio) or []
            return render_template(f'{PATH_URL}/detalles_municipio.html', detalle_municipio=detalle_municipio)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de municipios
@app.route("/buscando-municipio", methods=['POST'])
def viewBuscarMunicipioBD():
    resultadoBusqueda = buscarMunicipioBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_municipio.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-municipio/<int:id>", methods=['GET'])
def viewEditarMunicipio(id):
    if 'conectado' in session:
        respuestaMunicipio = buscarMunicipioUnico(id)
        if respuestaMunicipio:
            return render_template(f'{PATH_URL}/form_municipio_update.html', respuestaMunicipio=respuestaMunicipio)
        else:
            flash('El municipio no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de municipio
@app.route('/actualizar-municipio', methods=['POST'])
def actualizarMunicipio():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_municipios'))

# Reporte Exportar a Excel 
@app.route("/descargar-informe-municipios/", methods=['GET'])
def reporteBDmun():
    if 'conectado' in session:
        return generarReporteExcelxmun()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
# Ruta para resetear tablas 
@app.route("/resetear-tablas/", methods=['POST']) 
def resetearTablasRoute(): 
    if 'conectado' in session: 
        resetearTablas() 
        flash('Tablas reseteadas correctamente.', 'success') 
        return redirect(url_for('inicio'))
    else: 
        flash('primero debes iniciar sesión.', 'error') 
        return redirect(url_for('inicio'))
    

