from flask import Flask, request, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Diccionario simple para guardar el estado de la conversación por usuario
    # En producción usarías una base de datos o Redis
    user_sessions = {}

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        user_message = data.get('message', '').strip()
        user_id = "user_123" # En un caso real, esto vendría del frontend

        if user_id not in user_sessions:
            user_sessions[user_id] = {'step': 0}

        step = user_sessions[user_id]['step']

        # Lógica de la prueba (paso a paso)
        if step == 0:
            user_sessions[user_id]['step'] = 1
            return jsonify({"reply": "¡Claro! Para empezar, ¿podrías decirme tu nombre?"})
        
        elif step == 1:
            user_sessions[user_id]['name'] = user_message
            user_sessions[user_id]['step'] = 2
            return jsonify({"reply": f"Mucho gusto, {user_message}. ¿Me podrías compartir tu número de teléfono?"})
        
        elif step == 2:
            user_sessions[user_id]['phone'] = user_message
            user_sessions[user_id]['step'] = 3
            return jsonify({"reply": "Perfecto. Finalmente, ¿cuál es el motivo de tu interés por contactarme?"})
        
        elif step == 3:
            name = user_sessions[user_id].get('name')
            phone = user_sessions[user_id].get('phone')
            # Aquí podrías guardar esto en un archivo, enviarlo por correo o a un CRM
            user_sessions[user_id]['step'] = 0 # Reiniciar
            return jsonify({"reply": f"¡Gracias, {name}! He recibido tu mensaje sobre '{user_message}'. Te contactaré al {phone} pronto."})

        return jsonify({"reply": "Hubo un error, intentemos de nuevo."})

    return app