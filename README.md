# API de Memoria Estructurada

Una API construida con FastAPI que funciona como memoria estructurada personal, utilizando ChromaDB como base de datos vectorial para organizar información por relevancia semántica.

## Módulos

1. **Módulo de Identidad y Psicología**: Almacena información sobre perfil cognitivo y estrategias mentales.
2. **Módulo de Negocios y Estrategia**: Guarda ideas, decisiones y planes de acción.
3. **Módulo de Recordatorios y URLs**: Almacena enlaces y tareas importantes.

## Requisitos

- Python 3.8+
- FastAPI
- ChromaDB
- Otras dependencias en `requirements.txt`

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd <nombre-del-repositorio>

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

## Documentación API

Una vez que la aplicación esté en ejecución, puedes acceder a la documentación Swagger UI en:

```
http://localhost:8000/docs
```

## Estructura del Proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── identity.py
│   │   ├── business.py
│   │   └── reminders.py
│   └── utils/
│       ├── __init__.py
│       └── embeddings.py
├── data/
│   └── chroma/
├── .env.example
├── requirements.txt
└── README.md
``` 