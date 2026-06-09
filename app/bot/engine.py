def process_message(message, step, data):
    if not message:
        return 'Por favor, escribe algo válido.', step, data

    if message.lower() == 'reiniciar':
        return '¡Hola de nuevo! Reiniciemos el registro. ¿Cuál es tu nombre?', 1, {}

    if step == 1:
        data['name'] = message
        reply = f'Mucho gusto, {message}. ¿A qué correo o WhatsApp corporativo te puedo contactar?'
        return reply, 2, data

    elif step == 2:
        data['contact'] = message
        reply = 'Entendido. Cuéntame brevemente, ¿qué tipo de bot o automatización de procesos necesita tu negocio?'
        return reply, 3, data

    elif step == 3:
        data['requirement'] = message
        reply = f'Perfecto {data.get("name")}. He registrado tus requerimientos. Elige la hora de nuestra sesión aquí: [Tu Link de Calendly o Cal.com]'
        return reply, 4, data

    else:
        return 'Tu solicitud ya fue procesada con éxito. Si deseas cambiar algo, escribe "reiniciar".', 4, data
