from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from app.database import db_manager
from app.utils.airtable import airtable_manager
from app.models.schemas import Item, ItemCreate, ItemUpdate, ItemList

router = APIRouter(
    prefix="/airtable",
    tags=["airtable"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/sync/{collection_key}/{item_id}", status_code=200)
async def sync_to_airtable(
    collection_key: str = Path(..., description="Clave de la colección en ChromaDB"),
    item_id: str = Path(..., description="ID del item a sincronizar")
):
    """
    Sincroniza un item específico de ChromaDB a Airtable.
    """
    try:
        # Obtener el item de ChromaDB
        item = db_manager.get_item(collection_key=collection_key, id=item_id)
        
        if not item:
            raise HTTPException(status_code=404, detail=f"Item con ID '{item_id}' no encontrado en la colección '{collection_key}'")
        
        # Sincronizar con Airtable
        result = airtable_manager.sync_to_airtable(
            collection_key=collection_key,
            item_id=item_id,
            item_data=item
        )
        
        return {
            "message": "Item sincronizado correctamente con Airtable",
            "airtable_record": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al sincronizar con Airtable: {str(e)}")

@router.post("/", response_model=Item, status_code=201)
async def create_item(
    item: ItemCreate = Body(...),
    collection_key: str = Query(..., description="Clave de la colección en ChromaDB")
):
    """
    Crea un nuevo item en ChromaDB y lo sincroniza con Airtable.
    """
    try:
        # Generar ID único
        item_id = str(uuid.uuid4())
        
        # Añadir a ChromaDB
        chroma_result = db_manager.add_item(
            collection_key=collection_key,
            id=item_id,
            text=item.text,
            metadata=item.metadata
        )
        
        # Sincronizar con Airtable
        airtable_manager.sync_to_airtable(
            collection_key=collection_key,
            item_id=item_id,
            item_data=chroma_result
        )
        
        return chroma_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el item: {str(e)}")

@router.get("/", response_model=List[Dict[str, Any]])
async def list_airtable_records(
    max_records: Optional[int] = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    formula: Optional[str] = Query(None, description="Fórmula de filtrado para Airtable")
):
    """
    Lista todos los registros de Airtable.
    """
    try:
        records = airtable_manager.list_records(formula=formula, max_records=max_records)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar registros de Airtable: {str(e)}")

@router.get("/{record_id}")
async def get_airtable_record(
    record_id: str = Path(..., description="ID del registro en Airtable")
):
    """
    Obtiene un registro específico de Airtable.
    """
    try:
        record = airtable_manager.get_record(record_id)
        return record
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener registro de Airtable: {str(e)}")

@router.put("/{record_id}")
async def update_airtable_record(
    record_id: str = Path(..., description="ID del registro en Airtable"),
    fields: Dict[str, Any] = Body(..., description="Campos a actualizar")
):
    """
    Actualiza un registro existente en Airtable.
    """
    try:
        record = airtable_manager.update_record(record_id, fields)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar registro en Airtable: {str(e)}")

@router.delete("/{record_id}")
async def delete_airtable_record(
    record_id: str = Path(..., description="ID del registro en Airtable")
):
    """
    Elimina un registro de Airtable.
    """
    try:
        result = airtable_manager.delete_record(record_id)
        return {"message": "Registro eliminado correctamente", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar registro en Airtable: {str(e)}")

@router.post("/sync-from-airtable/{record_id}/{collection_key}")
async def sync_from_airtable(
    record_id: str = Path(..., description="ID del registro en Airtable"),
    collection_key: str = Path(..., description="Clave de la colección en ChromaDB")
):
    """
    Sincroniza un registro de Airtable a ChromaDB.
    """
    try:
        # Obtener datos de Airtable
        item_data = airtable_manager.sync_from_airtable(record_id)
        
        if not item_data.get("item_id"):
            raise HTTPException(status_code=400, detail="El registro de Airtable no contiene un ID de item válido")
        
        # Verificar si el item ya existe en ChromaDB
        existing_item = db_manager.get_item(
            collection_key=collection_key,
            id=item_data["item_id"]
        )
        
        if existing_item:
            # Actualizar el item existente
            result = db_manager.update_item(
                collection_key=collection_key,
                id=item_data["item_id"],
                text=item_data["text"],
                metadata=item_data["metadata"]
            )
        else:
            # Crear un nuevo item
            result = db_manager.add_item(
                collection_key=collection_key,
                id=item_data["item_id"],
                text=item_data["text"],
                metadata=item_data["metadata"]
            )
        
        return {
            "message": "Registro sincronizado correctamente con ChromaDB",
            "chroma_item": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al sincronizar desde Airtable: {str(e)}")