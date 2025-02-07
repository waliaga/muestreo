from flask import request, jsonify
from controllers.funciones_hexagonos import generar_muestras_aleatorias

@app.route('/generar-muestras-aleatorias', methods=['POST'])
def generar_muestras_aleatorias_route():
    if generar_muestras_aleatorias():
        return jsonify({"success": True, "message": "Muestras generadas correctamente."})
    else:
        return jsonify({"success": False, "message": "Error al generar las muestras."}), 500





import random
from conexion.conexionBD import connectionBD

def generar_muestras_aleatorias():
    try:
        with connectionBD() as conexion_PostgreSQLdb:
            with conexion_PostgreSQLdb.cursor() as cursor:
                # Paso inicial: vaciar sorteos en 0
                cursor.execute("""
                    UPDATE unodc_parcelas 
                    SET sorteado = 0, seleccionado = 0, sup_muestra = 0, num_muestra = 0 
                    WHERE true
                """)
                conexion_PostgreSQLdb.commit()

                # Recorrer municipios seleccionados
                cursor.execute("SELECT * FROM unodc_municipios WHERE seleccionado = 1")
                municipios = cursor.fetchall()

                for municipio in municipios:
                    cod_mun = municipio['cod_mun']
                    sup_muestra_mun = municipio['sup_muestra']

                    # Inicializamos la variable de la suma de las parcelas seleccionadas
                    suma_par = 0

                    # Recorremos las parcelas del municipio ordenadas por superficie y densidad
                    cursor.execute("""
                        SELECT * FROM unodc_parcelas 
                        WHERE cod_mun = %s 
                        ORDER BY densidad DESC, sup_parcelas
                    """, (cod_mun,))
                    parcelas = cursor.fetchall()

                    # Creamos un array para almacenar las parcelas con sus respectivos pesos
                    parcelas_con_pesos = []

                    # Almacenamos las parcelas y su peso basado en la densidad
                    for parcela in parcelas:
                        sup_parcelas = parcela['sup_parcelas']
                        densidad = parcela['densidad']
                        id_parcela = parcela['id']

                        # Asignar peso según la densidad
                        if densidad == 3:       # Alta densidad
                            peso = 30
                        elif densidad == 2:     # Media densidad
                            peso = 15
                        elif densidad == 1:     # Baja Densidad 
                            peso = 1

                        # Añadir la parcela y su peso al array
                        parcelas_con_pesos.append({
                            'id': id_parcela,
                            'sup_parcelas': sup_parcelas,
                            'peso': peso
                        })

                    # Empezamos a seleccionar las parcelas
                    while len(parcelas_con_pesos) > 0:
                        # Elegimos una parcela aleatoriamente, ponderada por su peso
                        total_peso = sum(parcela['peso'] for parcela in parcelas_con_pesos)
                        random_peso = random.randint(1, total_peso)

                        suma_peso = 0
                        seleccionada = None

                        # Buscamos la parcela cuya ponderación incluye el número aleatorio generado
                        for parcela in parcelas_con_pesos:
                            suma_peso += parcela['peso']
                            if suma_peso >= random_peso:
                                seleccionada = parcela
                                break

                        # Verificamos si podemos seleccionar la parcela sin exceder la muestra
                        if suma_par + seleccionada['sup_parcelas'] <= sup_muestra_mun:
                            # Actualizamos la parcela seleccionada
                            cursor.execute("""
                                UPDATE unodc_parcelas 
                                SET sorteado = sorteado + 1, 
                                    sup_muestra = %s, 
                                    num_muestra = num_parcelas, 
                                    seleccionado = 1 
                                WHERE id = %s
                            """, (seleccionada['sup_parcelas'], seleccionada['id']))
                            conexion_PostgreSQLdb.commit()

                            # Acumulamos la superficie seleccionada
                            suma_par += seleccionada['sup_parcelas']

                        # Si ya hemos alcanzado el límite de la muestra, salimos del ciclo
                        if suma_par >= sup_muestra_mun:
                            break

                        # Eliminar la parcela seleccionada de las opciones disponibles
                        parcelas_con_pesos = [parcela for parcela in parcelas_con_pesos if parcela['id'] != seleccionada['id']]

                # Actualizamos el shape "region22xls-point" en POSTGIS
                cursor.execute("UPDATE parcelas SET seleccionado = 0 WHERE TRUE")
                cursor.execute("""
                    UPDATE parcelas 
                    SET seleccionado = 1
                    FROM unodc_parcelas
                    WHERE parcelas.cod_hex = unodc_parcelas.cod_hex AND unodc_parcelas.seleccionado = 1
                """)
                conexion_PostgreSQLdb.commit()

        return True
    except Exception as e:
        print(f"Error en la función generar_muestras_aleatorias: {e}")
        return False
    
    <!-- Botón para sortear -->
<div class="col-md-6 text-start">
    <form action="/generar-muestras-aleatorias" method="POST">
        <button type="submit" class="btn btn-warning" title="Resetear Tablas">
            <i class="bi bi-arrow-counterclockwise"></i>
            Sortear Hexagonos
        </button>
    </form>
</div>

************



@app.route('/generar-muestras-aleatorias', methods=['POST'])
def generar_muestras_aleatorias_route():
    if generar_muestras_aleatorias():
        return jsonify({"success": True, "message": "Muestras generadas correctamente."})
    else:
        return jsonify({"success": False, "message": "Error al generar las muestras."}), 500





