import requests
import os

def enviar_notificacion_telegram(nombre, telefono, correo, motivo):
    # Obtenemos las variables de entorno configuradas en Render
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    
    # Validación de seguridad
    if not token or not chat_id:
        print("ERROR CRÍTICO: Las variables TELEGRAM_TOKEN o CHAT_ID no están configuradas.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Limpiamos los datos para evitar errores de Markdown en Telegram
    mensaje = (
        f"🔔 *Nuevo Lead Recibido:*\n\n"
        f"👤 *Nombre:* {nombre or 'No proporcionado'}\n"
        f"📞 *Teléfono:* {telefono or 'No proporcionado'}\n"
        f"📧 *Correo:* {correo or 'No proporcionado'}\n"
        f"💬 *Motivo:* {motivo or 'No proporcionado'}"
    )
    
    payload = {
        "chat_id": chat_id, 
        "text": mensaje, 
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10) # Timeout para evitar que se quede pegado
        if response.status_code == 200:
            print("✅ Notificación enviada con éxito a Telegram.")
            return True
        else:
            print(f"❌ Error al enviar a Telegram: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Excepción crítica al conectar con Telegram: {e}")
        return False