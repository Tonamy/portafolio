from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    # Habilitar CORS para permitir que tu frontend en Vue se comunique
    CORS(app, resources={r"/chat": {"origins": "*"}})

    @app.route('/chat', methods=['POST'])
    def chat():
        # Aquí irá tu lógica de IA más adelante
        return {"reply": "Conexión exitosa desde el backend"}

    return app