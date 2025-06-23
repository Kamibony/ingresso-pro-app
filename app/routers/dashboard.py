from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.database_models import Prestador

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard/{provider_id}", response_class=HTMLResponse, tags=["Dashboard"])
async def get_provider_dashboard(request: Request, provider_id: int, db: Session = Depends(get_db)):
    prestador = db.query(Prestador).filter(Prestador.id == provider_id).first()
    if not prestador:
        raise HTTPException(status_code=404, detail="Prestador não encontrado")
    
    success_message = request.query_params.get('success_message', None)
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
    db.refresh(prestador)
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "prestador": prestador, "success_message": "Alterações salvas com sucesso!"})
