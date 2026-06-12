from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from .chatbot_engine import enviar_notificacion_telegram 

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    user_sessions = {}

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Mensaje no recibido"}), 400
            
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'user_123') 

        if user_id not in user_sessions:
            user_sessions[user_id] = {'step': 0}
        
        session = user_sessions[user_id]
        step = session.get('step', 0)

        # Flujo de conversación
        if step == 0:
            session['step'] = 1
            reply = "¡Hola! Para empezar, ¿podrías decirme tu nombre?"
        elif step == 1:
            session['name'] = user_message
            session['step'] = 2
            reply = "Mucho gusto. ¿Me podrías compartir tu número de teléfono?"
        elif step == 2:
            session['phone'] = user_message
            session['step'] = 3
            reply = "Perfecto, ¿cuál es tu correo electrónico?"
        elif step == 3:
            session['email'] = user_message
            session['step'] = 4
            reply = "Gracias. Finalmente, ¿cuál es el motivo de tu interés?"
        elif step == 4:
            success = enviar_notificacion_telegram(session.get('name'), session.get('phone'), session.get('email'), user_message)
            reply = f"¡Gracias, {session.get('name')}! Recibí tu mensaje." if success else "Error técnico al enviar."
            session['step'] = 0 
        else:
            reply = "Error en el flujo."
            session['step'] = 0
        
        return jsonify({"reply": reply, "step": session['step']})

    @app.route('/', methods=['GET'])
    def index():
        # Asegúrate de que el archivo 'chat.html' esté en la carpeta 'templates'
        return render_template('chat.html')

    return app