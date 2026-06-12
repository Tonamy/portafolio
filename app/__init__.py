from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def index():
        return "El backend está funcionando correctamente."

    @app.route('/chat', methods=['POST'])
    def chat():
        # Aquí tu lógica
        return {"reply": "Hola, recibí tu mensaje"}

    return app