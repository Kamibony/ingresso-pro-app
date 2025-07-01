from fastapi import APIRouter, HTTPException
from typing import List
from app.models.pydantic_models import Sessao
from app.services import session_service

router = APIRouter()

@router.post("/eventos/{evento_id}/sessoes/", response_model=Sessao, tags=["Sessões"])
def endpoint_criar_sessao(evento_id: str, sessao: Sessao):
    """
    Cria uma nova sessão para um evento específico.
    O evento_id vem da URL.
    """
    try:
        return session_service.criar_sessao(evento_id, sessao)
    except Exception as e:
        # Adiciona um log mais detalhado do erro
        print(f"ERRO NO ENDPOINT: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar sessão: {e}")

@router.get("/eventos/{evento_id}/sessoes/", response_model=List[Sessao], tags=["Sessões"])
def endpoint_listar_sessoes(evento_id: str):
    """
    Lista todas as sessões de um evento específico.
    """
    try:
        return session_service.listar_sessoes_por_evento(evento_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar sessões: {e}")
