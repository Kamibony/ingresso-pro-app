# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.database_models import Prestador

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/{prestador_id}", summary="Exibe o painel de um prestador")
async def get_dashboard(request: Request, prestador_id: int, db: Session = Depends(get_db), success: bool = False):
    prestador = db.query(Prestador).filter(Prestador.id == prestador_id).first()
    if not prestador:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Prestador não encontrado"})

    success_message = "Alterações salvas com sucesso!" if success else None
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "prestador": prestador,
        "success_message": success_message
    })

@router.post("/dashboard/{prestador_id}", summary="Atualiza as informações de um prestador")
async def update_dashboard(
    prestador_id: int, db: Session = Depends(get_db), nome: str = Form(...),
    telefone: str = Form(...), especialidades: str = Form(...),
    disponibilidade: str = Form(...), observacao: str = Form(...)
):
    prestador = db.query(Prestador).filter(Prestador.id == prestador_id).first()
    if prestador:
        prestador.nome = nome
        prestador.telefone = telefone
        prestador.especialidades = [spec.strip() for spec in especialidades.split(',')]
        prestador.disponibilidade = disponibilidade
        prestador.observacao = observacao
        db.commit()
    return RedirectResponse(url=f"/dashboard/{prestador_id}?success=true", status_code=status.HTTP_303_SEE_OTHER)
