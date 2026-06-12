import requests
import os
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

def test_telegram():
    print(f"Probando con Token: {token[:10]}... y ChatID: {chat_id}")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "¡Hola! Esta es una prueba de conexión rápida.",
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ ¡Éxito! Telegram respondió 200 OK. El mensaje debió llegar.")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_telegram()