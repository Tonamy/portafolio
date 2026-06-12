"""
Base de conocimiento estática del perfil y proyectos de Tonatiuh Garza.

Este módulo se inyecta como contexto en el system prompt del LLM. Es la
ÚNICA fuente de verdad sobre proyectos: el modelo NO debe hablar de
proyectos que no estén listados aquí. Para añadir un proyecto nuevo,
basta con agregar un diccionario a PROYECTOS — no se requiere tocar
bot_brain.py.
"""

PERFIL = (
    "Tonatiuh Garza es especialista en Python, AsyncIO, REST APIs, Webhooks, "
    "ETL, integraciones SaaS, arquitecturas event-driven, automatización "
    "empresarial e IA Generativa (Gemini, Ollama). Cuenta con experiencia "
    "técnica en WhatsApp Business API, Google Apps Script, JavaScript, "
    "Pandas, y conectores hacia plataformas de gestión empresarial "
    "(CRM, ERP, ATS, HR)."
)

PROYECTOS = [
    {
        "nombre": "Sincronización ATS-CRM",
        "resumen": (
            "Sistema de sincronización en tiempo real entre plataformas "
            "mediante APIs REST y Webhooks."
        ),
        "capacidades": [
            "Integración de plataformas",
            "Sincronización bidireccional",
            "Persistencia de eventos",
            "Gestión de rate limits",
            "Manejo avanzado de errores",
            "Mapeo dinámico de datos",
        ],
    },
    {
        "nombre": "Automatización Conversacional",
        "resumen": (
            "Agentes conversacionales impulsados por IA para captura y "
            "procesamiento de información."
        ),
        "capacidades": [
            "Captura automática de información",
            "Extracción de datos estructurados",
            "Automatización de procesos",
            "Integraciones empresariales",
            "Agendamiento automatizado",
        ],
    },
    {
        "nombre": "Sistema de Gestión de Activos con QR",
        "resumen": (
            "Plataforma físico-digital para trazabilidad y auditoría de "
            "activos."
        ),
        "capacidades": [
            "QR dinámicos",
            "Extracción asíncrona",
            "Integración ERP",
            "Sincronización de datos",
            "Visualización en tiempo real",
        ],
    },
    {
        "nombre": "T.A.M.I.",
        "resumen": "Plataforma de inteligencia de mercado impulsada por IA.",
        "capacidades": [
            "Web scraping",
            "Google Trends",
            "Curación de contenido",
            "Construcción de datasets",
            "Integración con LLMs",
        ],
    },
    {
        "nombre": "Migraciones de Datos",
        "resumen": "Automatización de migraciones empresariales mediante ETL.",
        "capacidades": [
            "ETL",
            "Limpieza de datos",
            "Normalización",
            "Validación",
            "Auditoría",
        ],
    },
]


def construir_contexto_proyectos() -> str:
    """Genera un bloque de texto con los proyectos para el system prompt."""
    bloques = []
    for p in PROYECTOS:
        caps = ", ".join(p["capacidades"])
        bloques.append(f"- {p['nombre']}: {p['resumen']} Capacidades: {caps}.")
    return "\n".join(bloques)