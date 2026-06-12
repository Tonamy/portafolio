"""
Núcleo de IA del Asistente Estratégico de Tonatiuh Garza.
"""
from google import genai
from google.genai import types
import os
import logging
from dotenv import load_dotenv
from app.knowledge_base import PERFIL, construir_contexto_proyectos

load_dotenv()
logger = logging.getLogger(__name__)

# Configuración del Cliente y Modelo
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite")

# 1. Definición de la herramienta (Debe ir ANTES de las funciones que la usan)
EXTRACTION_TOOL = types.FunctionDeclaration(
    name="actualizar_datos_lead",
    description="Extrae nombre, teléfono, correo y motivo.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "nombre": {"type": "string"},
            "telefono": {"type": "string"},
            "correo": {"type": "string"},
            "motivo": {"type": "string"},
        },
    ),
)

MENSAJE_FALLBACK = "Disculpa, tuve un problema técnico momentáneo. ¿Podrías intentar de nuevo?"

# --- Funciones Auxiliares ---
def _historial_a_contents(historial):
    return [types.Content(role=t["role"], parts=[types.Part(text=p) for p in t["parts"]]) for t in historial]

# 2. Función de Extracción (Ahora sí conoce EXTRACTION_TOOL)
def extraer_datos(mensaje, datos_sesion):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"Usuario: {mensaje}",
            config=types.GenerateContentConfig(
                tools=[types.Tool(function_declarations=[EXTRACTION_TOOL])],
                system_instruction=f"Extrae datos del lead. Conocidos: {datos_sesion}",
            ),
        )
        if response.candidates and response.candidates[0].content.parts:
            fc = response.candidates[0].content.parts[0].function_call
            return {k: v for k, v in dict(fc.args).items() if v} if fc else {}
        return {}
    except Exception as e:
        logger.error(f"Error crítico en extracción: {e}")
        raise e  # Esto disparará el modo emergencia en el archivo __init__.py

# 3. Función de Respuesta IA
def obtener_respuesta_ia(historial, datos_sesion, mensaje_usuario):
    # Aquí iría tu lógica de SYSTEM_PROMPT_TEMPLATE (asegúrate de tenerla definida arriba o importada)
    from app.bot_brain import SYSTEM_PROMPT_TEMPLATE # Si la moviste
    
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        perfil=PERFIL, proyectos=construir_contexto_proyectos(), datos_sesion=datos_sesion
    )
    contents = _historial_a_contents(historial)
    contents.append(types.Content(role="user", parts=[types.Part(text=mensaje_usuario)]))
    
    try:
        response = client.models.generate_content(
            model=MODEL, 
            contents=contents, 
            config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
        return response.text.strip() if response.text else MENSAJE_FALLBACK
    except Exception as e:
        logger.error(f"Error IA: {e}")
        raise e