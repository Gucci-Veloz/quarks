from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import API_TITLE, API_DESCRIPTION, API_VERSION
from app.modules import identity, business, reminders, connections, learnings, priorities, suggestions, airtable

# Crear la aplicación FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de los módulos
app.include_router(identity.router)
app.include_router(business.router)
app.include_router(reminders.router)
app.include_router(connections.router)
app.include_router(learnings.router)
app.include_router(priorities.router)
app.include_router(suggestions.router)
app.include_router(airtable.router)

# Ruta raíz
@app.get("/")
async def root():
    """
    Ruta raíz que proporciona información básica sobre la API.
    """
    return {
        "name": API_TITLE,
        "description": API_DESCRIPTION,
        "version": API_VERSION,
        "documentation": "/docs",
        "modules": [
            {"name": "Identidad y Psicología", "endpoint": "/identity"},
            {"name": "Negocios y Estrategia", "endpoint": "/business"},
            {"name": "Recordatorios y URLs", "endpoint": "/reminders"},
            {"name": "Conexiones Inteligentes", "endpoint": "/conexiones"},
            {"name": "Aprendizajes y Reflexiones", "endpoint": "/aprendizajes"},
            {"name": "Priorización y Filtrado", "endpoint": "/prioridad"},
            {"name": "Sugerencias Inteligentes", "endpoint": "/sugerencias"},
            {"name": "Integración con Airtable", "endpoint": "/airtable"}
        ]
    }

# Manejador de excepciones global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejador global de excepciones.
    """
    # Registrar la excepción (en un sistema de producción, se usaría un logger)
    print(f"Error no manejado: {str(exc)}")
    
    # Devolver una respuesta de error genérica
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )

# Manejador de excepciones HTTP
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Manejador de excepciones HTTP.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Punto de entrada para ejecutar la aplicación con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)