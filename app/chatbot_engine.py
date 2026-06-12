import requests
import os

def enviar_notificacion_telegram(nombre, telefono, correo, motivo):
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    
    print(f"DEBUG: Token={token[:5]}..., ChatID={chat_id}") # Esto te dirá si las variables están cargando

    if not token or not chat_id:
        print("ERROR: Variables de entorno no encontradas.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    mensaje = f"🔔 *Nuevo Lead:*\n👤 {nombre}\n📞 {telefono}\n📧 {correo}\n💬 {motivo}"
    
    payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, json=payload)
        print(f"DEBUG: Respuesta Telegram: {response.status_code} - {response.text}") # ESTO ES CLAVE
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: Excepción en requests: {e}")
        return False