from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND

from ..database import get_db
from ..models.database_models import Prestador

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard/{provider_id}", response_class=HTMLResponse, tags=["Dashboard"])
async def get_provider_dashboard(request: Request, provider_id: int, db: Session = Depends(get_db)):
    prestador = db.query(Prestador).filter(Prestador.id == provider_id).first()
    if not prestador:
        raise HTTPException(status_code=404, detail="Prestador não encontrado")
    
    # Simplificando: A mensagem de sucesso será passada via query param
    success_message = request.query_params.get('success', None)
    return templates.TemplateResponse("dashboard.html", {"request": request, "prestador": prestador, "success_message": success_message})

@router.post("/dashboard/{provider_id}", response_class=HTMLResponse, tags=["Dashboard"])
async def update_provider_dashboard(request: Request, provider_id: int, db: Session = Depends(get_db),
                                  nome: str = Form(...),
                                  telefone: str = Form(...),
                                  especialidades: str = Form(...),
                                  disponibilidade: str = Form(...),
                                  observacao: str = Form(...)):
    prestador = db.query(Prestador).filter(Prestador.id == provider_id).first()
    if not prestador:
        raise HTTPException(status_code=404, detail="Prestador não encontrado")

    prestador.nome = nome
    prestador.telefone = telefone
    prestador.especialidades = [e.strip().lower() for e in especialidades.split(',')]
    prestador.disponibilidade = disponibilidade
    prestador.observacao = observacao

    db.commit()
    
    # CORREÇÃO: Redireciona para a mesma página com uma mensagem de sucesso na URL
    # Isso evita problemas de renderização e é uma prática web padrão.
    return RedirectResponse(
        url=f"/dashboard/{provider_id}?success=true",
        status_code=HTTP_302_FOUND
    )
