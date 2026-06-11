from flask import Flask
from flask_cors import CORS # 1. Importa la librería

def create_app():
    app = Flask(__name__)
    
    # 2. Habilita CORS para todas las rutas
    # Esto le dice a tu navegador: "Confía en las peticiones que vienen desde cualquier sitio"
    CORS(app) 
    
    # ... resto de tu código ...
    
    return app