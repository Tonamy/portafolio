import os

# 1. Definir la estructura modular de carpetas
folders = [
    "app",
    "app/bot",
    "app/integrations",
    "app/templates",
    "web_portfolio"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 2. Definir los archivos con configuraciones para Local y Nube (Render)
files_content = {
    # .gitignore le dice a Git qué carpetas NO debe subir a GitHub
    ".gitignore": (
        "venv/\n"
        "*.pyc\n"
        "__pycache__/\n"
        ".env\n"
    ),
    
    # Requerimientos listos para producción en Render
    "requirements.txt": (
        "Flask==3.0.3\n"
        "gunicorn==23.0.0\n"
    ),
    
    # Punto de entrada para Flask y Gunicorn
    "run.py": (
        "from app import create_app\n\n"
        "app = create_app()\n\n"
        "if __name__ == '__main__':\n"
        "    # Local corren en el puerto 5000\n"
        "    app.run(host='0.0.0.0', port=5000, debug=True)\n"
    ),
    
    "app/__init__.py": (
        "from flask import Flask\n\n"
        "def create_app():\n"
        "    app = Flask(__name__)\n"
        "    from app.routes import main_blueprint\n"
        "    app.register_blueprint(main_blueprint)\n"
        "    return app\n"
    ),
    
    "app/bot/__init__.py": "",
    "app/integrations/__init__.py": "",
    
    # Módulo preparado para futuras integraciones de APIs
    "app/integrations/hubspot.py": (
        "def sync_lead_to_hubspot(name, contact, requirement):\n"
        "    # Aquí conectaremos la API de HubSpot más adelante\n"
        "    pass\n"
    ),
    
    # Máquina de estados del bot conversacional
    "app/bot/engine.py": (
        "def process_message(message, step, data):\n"
        "    if not message:\n"
        "        return 'Por favor, escribe algo válido.', step, data\n\n"
        "    if message.lower() == 'reiniciar':\n"
        "        return '¡Hola de nuevo! Reiniciemos el registro. ¿Cuál es tu nombre?', 1, {}\n\n"
        "    if step == 1:\n"
        "        data['name'] = message\n"
        "        reply = f'Mucho gusto, {message}. ¿A qué correo o WhatsApp corporativo te puedo contactar?'\n"
        "        return reply, 2, data\n\n"
        "    elif step == 2:\n"
        "        data['contact'] = message\n"
        "        reply = 'Entendido. Cuéntame brevemente, ¿qué tipo de bot o automatización de procesos necesita tu negocio?'\n"
        "        return reply, 3, data\n\n"
        "    elif step == 3:\n"
        "        data['requirement'] = message\n"
        "        reply = f'Perfecto {data.get(\"name\")}. He registrado tus requerimientos. Elige la hora de nuestra sesión aquí: [Tu Link de Calendly o Cal.com]'\n"
        "        return reply, 4, data\n\n"
        "    else:\n"
        "        return 'Tu solicitud ya fue procesada con éxito. Si deseas cambiar algo, escribe \"reiniciar\".', 4, data\n"
    ),
    
    # Endpoints HTTP
    "app/routes.py": (
        "from flask import Blueprint, request, jsonify, render_template\n\n"
        "main_blueprint = Blueprint('main', __name__)\n\n"
        "@main_blueprint.route('/')\n"
        "def home():\n"
        "    return render_template('chat.html')\n\n"
        "@main_blueprint.route('/chat', methods=['POST'])\n"
        "def chat_handler():\n"
        "    from app.bot.engine import process_message\n"
        "    request_data = request.get_json() or {}\n"
        "    user_message = request_data.get('message', '').strip()\n"
        "    step = request_data.get('step', 1)\n"
        "    data = request_data.get('data', {})\n"
        "    reply, next_step, updated_data = process_message(user_message, step, data)\n"
        "    return jsonify({'reply': reply, 'next_step': next_step, 'data': updated_data})\n"
    ),
    
    # Interfaz del Chat (Responsiva y limpia)
    "app/templates/chat.html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 15px; background: #f8fafc; display: flex; flex-direction: column; height: 93vh; }
        #chatbox { flex: 1; border: 1px solid #e2e8f0; background: white; overflow-y: auto; padding: 15px; border-radius: 8px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); }
        #input-area { margin-top: 10px; display: flex; gap: 8px; }
        #message { flex: 1; padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 14px; outline: none; }
        #message:focus { border-color: #3b82f6; }
        #send-btn { padding: 12px 20px; background: #3b82f6; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
        .msg { margin: 10px 0; padding: 10px 14px; border-radius: 8px; max-width: 75%; line-height: 1.4; font-size: 14px; }
        .bot { background: #f1f5f9; color: #1e293b; align-self: flex-start; margin-right: auto; }
        .user { background: #3b82f6; color: white; margin-left: auto; text-align: left; }
    </style>
</head>
<body>
    <div id="chatbox" style="display: flex; flex-direction: column;">
        <div class="msg bot"><b>Asistente:</b> ¡Hola! Soy el asistente automatizado de Tonatiuh. ¿Con quién tengo el gusto?</div>
    </div>
    <div id="input-area">
        <input type="text" id="message" placeholder="Escribe tu respuesta..." onkeypress="if(event.key === 'Enter') sendMessage()">
        <button id="send-btn" onclick="sendMessage()">Enviar</button>
    </div>
    <script>
        let step = 1;
        let userData = {};
        function sendMessage() {
            const input = document.getElementById('message');
            const text = input.value.trim();
            if(!text) return;
            appendMessage(text, 'user');
            input.value = '';
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: text, step: step, data: userData })
            })
            .then(res => res.json())
            .then(resData => {
                appendMessage(resData.reply, 'bot');
                step = resData.next_step;
                userData = resData.data;
            }).catch(err => {
                appendMessage("Error de conexión con el servidor.", 'bot');
            });
        }
        function appendMessage(text, sender) {
            const chatbox = document.getElementById('chatbox');
            const msgDiv = document.createElement('div');
            msgDiv.className = `msg ${sender}`;
            msgDiv.innerHTML = text.replace(/\\[(.*?)\\]/g, '<a href="https://calendly.com" target="_blank" style="color:#3b82f6; font-weight:bold;">$1</a>');
            chatbox.appendChild(msgDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>""",
    
    # Portafolio Web Embebiendo el localhost (Temporal antes de subir a Render)
    "web_portfolio/index.html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tonatiuh Garza | Automatización & Arquitectura Técnica</title>
    <style>
        body { margin: 0; padding: 0; font-family: 'Arial', sans-serif; background-color: #f4f6f9; color: #1a202c; }
        .header { background-color: #0f172a; color: #ffffff; padding: 30px 20px; text-align: center; border-bottom: 4px solid #3b82f6; }
        .header h1 { margin: 0; font-size: 24px; }
        .container { max-width: 800px; margin: 25px auto; padding: 0 20px; }
        .card { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); padding: 24px; margin-bottom: 25px; border-left: 5px solid #3b82f6; }
        .chat-container { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #e2e8f0; height: 500px; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Tonatiuh Garza Martinez</h1>
        <p>Technical Architect & Automation Specialist</p>
    </div>
    <div class="container">
        <div class="card">
            <h2>Demostración en Vivo: Bot de Agendamiento Comercial</h2>
            <p>Este asistente conversacional interactúa con clientes en tiempo real y sincroniza las citas directamente en el calendario.</p>
        </div>
        <div class="chat-container">
            <iframe src="http://localhost:5000" title="Bot de Agendamiento"></iframe>
        </div>
    </div>
</body>
</html>"""
}

# 3. Escribir y sobreescribir los archivos con codificación limpia
for filepath, content in files_content.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("¡Estructura de producción local y nube creada exitosamente!")