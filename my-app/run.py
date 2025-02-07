# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
from app import app
from app import create_app
app = create_app()

# Importando todos mis Routers (Rutas)
from routers.router_login import *
from routers.router_mapas import *
from routers.router_municipios import *
from routers.router_hexagonos import *
from routers.router_usuarios import *
from routers.router_page_not_found import *
# Importa las rutas import


# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5600) # Para ejecutar en la red local - DESARROLLO
    #app.run(host='10.1.2.65', port=5000)
