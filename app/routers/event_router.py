from fastapi import APIRouter, HTTPException
from typing import List
from app.models.pydantic_models import Evento
from app.services import event_service

router = APIRouter()

@router.post("/eventos/", response_model=Evento, tags=["Eventos"])
def endpoint_criar_evento(evento: Evento):
    """
    Cria um novo evento no sistema.
    """
    try:
        return event_service.criar_evento(evento)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar evento: {e}")

@router.get("/eventos/", response_model=List[Evento], tags=["Eventos"])
def endpoint_listar_eventos():
    """
    Lista todos os eventos cadastrados.
    """
    try:
        return event_service.listar_eventos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar eventos: {e}")
