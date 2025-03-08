from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
from app.config import EMBEDDING_MODEL

def get_embedding_function():
    """
    Retorna una función de embedding para ChromaDB.
    
    Utiliza el modelo de SentenceTransformers especificado en la configuración.
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

def get_embedding_model():
    """
    Retorna el modelo de SentenceTransformers para generar embeddings.
    
    Útil cuando se necesita acceso directo al modelo para operaciones
    más avanzadas que las proporcionadas por ChromaDB.
    """
    return SentenceTransformer(EMBEDDING_MODEL) 