# Importamos la función de integración
from app.chatbot_engine import enviar_notificacion_telegram

STATE_START = "START"
STATE_GET_NAME = "GET_NAME"
STATE_GET_PHONE = "GET_PHONE"
STATE_GET_EMAIL = "GET_EMAIL"
STATE_GET_MOTIVE = "GET_MOTIVE"
STATE_COMPLETED = "COMPLETED"

def get_next_step(current_state, user_message, session_data):
    reply = ""
    next_state = current_state

    if current_state == STATE_START:
        next_state = STATE_GET_NAME
        reply = "¡Hola! Para empezar, ¿podrías decirme tu nombre?"
        
    elif current_state == STATE_GET_NAME:
        session_data['name'] = user_message
        next_state = STATE_GET_PHONE
        reply = f"Mucho gusto, {user_message}. ¿Me podrías compartir tu número de teléfono?"
        
    elif current_state == STATE_GET_PHONE:
        session_data['phone'] = user_message
        next_state = STATE_GET_EMAIL
        reply = "Perfecto, ¿cuál es tu correo electrónico?"
        
    elif current_state == STATE_GET_EMAIL:
        session_data['email'] = user_message
        next_state = STATE_GET_MOTIVE
        reply = "Gracias. Finalmente, ¿cuál es el motivo de tu interés?"
        
    elif current_state == STATE_GET_MOTIVE:
        session_data['motive'] = user_message
        
        # --- AQUÍ EJECUTAMOS LA INTEGRACIÓN ---
        success = enviar_notificacion_telegram(
            session_data.get('name'), 
            session_data.get('phone'), 
            session_data.get('email'), 
            session_data.get('motive')
        )
        
        next_state = STATE_COMPLETED
        if success:
            reply = f"¡Gracias, {session_data.get('name')}! Tu solicitud ha sido enviada con éxito."
        else:
            reply = "Gracias, pero hubo un problema técnico al enviar tu solicitud. Intentaremos procesarla manualmente."
    
    elif current_state == STATE_COMPLETED:
        # Reiniciamos el ciclo para una nueva interacción
        session_data.clear()
        next_state = STATE_GET_NAME
        reply = "¡Hola de nuevo! Si deseas registrar una nueva solicitud, por favor dime tu nombre."
    
    return reply, next_state, session_data