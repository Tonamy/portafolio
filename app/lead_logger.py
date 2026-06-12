"""
Persistencia de eventos de leads.

Usa SQLite (un único archivo `leads.db`) en lugar de un .txt con append.
Ventajas sobre el archivo plano:
- Escrituras atómicas y seguras con múltiples workers/threads.
- Permite consultar leads completos fácilmente (sqlite3 CLI, DB Browser,
  o un futuro endpoint de administración) sin parsear JSON línea por línea.
- Sigue siendo "un solo archivo", sin servicios adicionales que mantener.
"""

import sqlite3
import datetime
import os
import threading

DB_PATH = os.environ.get("LEADS_DB_PATH", "leads.db")

_lock = threading.Lock()


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            session_id TEXT NOT NULL,
            nombre TEXT,
            telefono TEXT,
            correo TEXT,
            motivo TEXT,
            status TEXT NOT NULL
        )
        """
    )
    return conn


def registrar_evento(session_id: str, datos: dict, status: str = "parcial") -> None:
    """
    Inserta un nuevo registro de evento del lead.

    Se inserta un nuevo row por cada llamada (no se actualiza en sitio)
    para conservar el historial de evolución del lead a lo largo de la
    conversación, igual que el archivo .txt original pero consultable.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with _lock:
        conn = _get_connection()
        try:
            conn.execute(
                """
                INSERT INTO leads
                    (timestamp, session_id, nombre, telefono, correo, motivo, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    timestamp,
                    session_id,
                    datos.get("nombre"),
                    datos.get("telefono"),
                    datos.get("correo"),
                    datos.get("motivo"),
                    status,
                ),
            )
            conn.commit()
        finally:
            conn.close()