import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de la API
API_TITLE = "API de Memoria Estructurada"
API_DESCRIPTION = "API para almacenar y recuperar información personal estructurada"
API_VERSION = "0.1.0"

# Configuración de ChromaDB
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", str(BASE_DIR / "data" / "chroma"))

# Configuración de embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Nombres de las colecciones en ChromaDB
COLLECTIONS = {
    "identity": "identity_psychology",
    "business": "business_strategy",
    "reminders": "reminders_urls",
    "connections": "smart_connections",
    "learnings": "learnings_reflections",
    "priorities": "priority_filtering",
    "suggestions": "smart_suggestions"
} 

# Configuración de Airtable
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_ID = os.getenv("AIRTABLE_TABLE_ID", "tbln3teMfz1sbqIuf")