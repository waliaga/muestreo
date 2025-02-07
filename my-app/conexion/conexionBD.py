# Python con PostgreSQL
# Importando Libreria psycopg2 para conectar Python con PostgreSQL
import psycopg2


def connectionBD():
    try:
        # Parámetros de conexión a PostgreSQL
        connection = psycopg2.connect(
            host="dpg-cuj5bhl2ng1s73f5i57g-a.oregon-postgres.render.com",       # Host de la base de datos
            user="muestreo_user",                                               # Usuario de la base de datos
            password="uTGpAYWSsEIaAdgXsS2P7Inxv6aj0vDS",                        # Contraseña del usuario
            database="muestreo",                                                # Nombre de la base de datos
            port="5432"                                                         # Puerto de PostgreSQL (por defecto es 5432)
        )
        
        # Verificar si la conexión fue exitosa
        if connection:
            # print("Conexión exitosa a la BD")
            return connection

    except psycopg2.Error as error:
        print(f"No se pudo conectar: {error}")


