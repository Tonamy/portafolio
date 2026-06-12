"""
Servicio de notificación de leads vía Telegram.

Esta es la ÚNICA implementación de notificación del proyecto. La versión
duplicada que existía en chatbot_engine.py fue eliminada para evitar
inconsistencias y posibles notificaciones duplicadas.
"""

import requests
import os
import logging

logger = logging.getLogger(__name__)


def enviar_notificacion(datos: dict) -> bool:
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    if not token or not chat_id:
        logger.warning(
            "TELEGRAM_TOKEN o CHAT_ID no configurados; no se envía notificación."
        )
        return False

    mensaje = (
        "🔔 *Nuevo Lead:*\n"
        f"👤 Nombre: {datos.get('nombre')}\n"
        f"📞 Tel: {datos.get('telefono')}\n"
        f"📧 Mail: {datos.get('correo')}\n"
        f"💬 Motivo: {datos.get('motivo')}"
    )
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        resp = requests.post(
            url,
            json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"},
            timeout=10,
        )
        if resp.status_code != 200:
            logger.error(
                "Telegram respondió con error %s: %s", resp.status_code, resp.text
            )
            return False
        return True
    except requests.RequestException:
        logger.exception("Error de red enviando notificación a Telegram")
        return False