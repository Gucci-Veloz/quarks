import os
import pytest
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.utils.auth import create_access_token
from app.config import SOFIA_API_KEY, AUTH_SECRET_KEY

# Sobrescribir la clave API de SofIA para pruebas
os.environ["SOFIA_API_KEY"] = "test_sofia_api_key"

# Crear un directorio temporal para ChromaDB durante las pruebas
@pytest.fixture(scope="session")
def temp_chroma_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["CHROMA_DB_DIR"] = temp_dir
        yield temp_dir

@pytest.fixture
def client(temp_chroma_dir):
    """Cliente de prueba para la API FastAPI."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def auth_token():
    """Token JWT de autenticación para pruebas."""
    token = create_access_token(data={"sub": "testuser", "scopes": ["read", "write"]})
    return token

@pytest.fixture
def auth_headers(auth_token):
    """Encabezados con token de autenticación para pruebas."""
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def api_key_headers():
    """Encabezados con API Key para pruebas."""
    return {"X-API-Key": "test_sofia_api_key"}

@pytest.fixture
def test_item():
    """Item de prueba para crear en la base de datos."""
    return {
        "text": "Esto es un texto de prueba para QUARK",
        "collection": "identity",
        "metadata": {
            "category": "test",
            "priority": "medium",
            "tags": ["test", "quark", "api"]
        }
    }

@pytest.fixture
def created_test_item(client, api_key_headers, test_item):
    """Crea un item de prueba y lo devuelve."""
    response = client.post("/sofia/store", headers=api_key_headers, json=test_item)
    if response.status_code != 201:
        pytest.fail(f"Error al crear item de prueba: {response.text}")
    return response.json() 