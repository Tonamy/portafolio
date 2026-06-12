from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from app.bot_brain import obtener_respuesta_ia, extraer_datos
from app.lead_logger import registrar_evento
from app.telegram_service import enviar_notificacion
import os, uuid, logging

logging.basicConfig(level=logging.INFO)
MAX_HISTORIAL = 20

MSG_EMERGENCIA = "¡Hola! Actualmente estoy atendiendo procesos de forma personalizada y mi asistente virtual está en pausa técnica. Para dedicarle tiempo a tu proyecto, por favor escríbeme directamente por WhatsApp al **7292813321**. ¡Será un gusto conversar contigo!"

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY")

    # NUEVA RUTA PARA SERVIR TU INDEX.HTML
    @app.route("/")
    def index():
        # Estamos en 'app/', subimos un nivel a la raíz ('..') 
        # y entramos a 'web_portfolio/' para buscar el archivo
        return send_from_directory(os.path.join(app.root_path, '../web_portfolio'), 'index.html')

    @app.route("/chat", methods=["POST", "OPTIONS"])
    def chat():
        if request.method == "OPTIONS": return jsonify({}), 200
        
        # ... (Toda tu lógica de chat se queda EXACTAMENTE IGUAL)
        body = request.get_json(silent=True) or {}
        message = (body.get("message") or "").strip()
        if not message: return jsonify({"reply": "¿Podrías escribir tu mensaje?"}), 200

        if "datos" not in session:
            session["datos"] = {"nombre": None, "telefono": None, "correo": None, "motivo": None}
            session["historial"] = []
            session["session_id"] = str(uuid.uuid4())
            session["notificado"] = False
            session["modo_emergencia"] = False

        if session.get("modo_emergencia"):
            return jsonify({"reply": MSG_EMERGENCIA})

        msg_low = message.lower()
        if any(w in msg_low for w in ["hola", "buen dia", "buenas tardes", "hey"]):
            return jsonify({"reply": "¡Hola! Soy el asistente virtual de Tonatiuh. ¿En qué proceso de automatización o IA estás trabajando?"})

        try:
            nuevos_datos = extraer_datos(message, session["datos"])
            for campo, valor in nuevos_datos.items():
                if campo in session["datos"] and valor: session["datos"][campo] = valor
            
            prompt_presion = " [INSTRUCCIÓN: Ya tienes el motivo, solicita nombre y teléfono]." if session["datos"].get("motivo") else ""
            respuesta = obtener_respuesta_ia(session["historial"], session["datos"], message + prompt_presion)
            
            session["historial"].append({"role": "user", "parts": [message]})
            session["historial"].append({"role": "model", "parts": [respuesta]})
            if len(session["historial"]) > MAX_HISTORIAL: session["historial"] = session["historial"][-MAX_HISTORIAL:]

            if session["datos"]["telefono"] and session["datos"]["nombre"] and not session.get("notificado"):
                if enviar_notificacion(session["datos"]):
                    session["notificado"] = True
                    registrar_evento(session["session_id"], session["datos"], status="completo")

            session.modified = True
            return jsonify({"reply": respuesta})

        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                session["modo_emergencia"] = True
                session.modified = True
                return jsonify({"reply": MSG_EMERGENCIA})
            return jsonify({"reply": "Disculpa, hubo un error técnico. ¿Podrías intentar de nuevo?"})

    return app