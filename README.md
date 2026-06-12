Este proyecto es una aplicación web personal que sirve como portafolio profesional, integrada con un chatbot automatizado capaz de captar leads y enviarlos directamente a Telegram.
🚀 Tecnologías Utilizadas

    Backend: Python, Flask

    Despliegue: Render

    Integración: API de Telegram

    Frontend: HTML5, CSS3, JavaScript (Fetch API)

    Servidor de Producción: Gunicorn

🏗️ Arquitectura del Sistema

El proyecto utiliza una arquitectura de servidor único donde Flask maneja tanto la renderización de la interfaz del portafolio como la lógica del chat.
🛠️ Cómo ejecutarlo localmente

    Clonar el repositorio:
    Bash

    git clone [URL-de-tu-repositorio]
    cd portafolio

    Crear entorno virtual:
    Bash

    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

    Instalar dependencias:
    Bash

    pip install -r requirements.txt

    Configurar variables de entorno:
    Crea un archivo .env en la raíz y agrega:
    Plaintext

    TELEGRAM_TOKEN=tu_token_aqui
    CHAT_ID=tu_chat_id_aqui

    Ejecutar:
    Bash

    python run.py

⚙️ Despliegue en Render

El proyecto está optimizado para despliegue automático en Render mediante un archivo Procfile.

    Build Command: pip install -r requirements.txt

    Start Command: gunicorn run:app

    Variables de Entorno: Deben ser configuradas en el panel de Environment de Render.

👤 Autor

    Tonatiuh Garza

    [[Enlace a tu LinkedIn]](https://www.linkedin.com/in/tonatiuh-garza-martinez-9b46a114b/)

    
