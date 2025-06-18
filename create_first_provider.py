# -*- coding: utf-8 -*-
from app.database import SessionLocal
from app.models.database_models import Prestador

db = SessionLocal()
print("Verificando se o prestador já existe...")
prestador_existente = db.query(Prestador).filter(Prestador.email == "carlos.andrade@email.com").first()

if prestador_existente:
    print("Dr. Carlos Andrade já existe no banco de dados.")
else:
    print("Criando o primeiro prestador: Dr. Carlos Andrade...")
    novo_prestador = Prestador(
        nome="Dr. Carlos Andrade", email="carlos.andrade@email.com", telefone="83 99999-0001",
        categoria="terapeuta", especialidades=["ansiedade", "depressão", "TCC"],
        bairro="Tambaú", disponibilidade="Segundas e Quartas à tarde.",
        observacao="Foco em Terapia Cognitivo-Comportamental (TCC) para adultos."
    )
    db.add(novo_prestador)
    db.commit()
    db.refresh(novo_prestador)
    print("Dr. Carlos Andrade adicionado com sucesso!")

db.close()
