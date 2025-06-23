from app.database import SessionLocal
from app.models.database_models import Prestador

banco_de_dados_mvp = [
    {
        "id": 1, "nome": "Dr. Carlos Andrade", "categoria": "terapeuta", "especialidades": ["ansiedade", "depressão", "tcc"], "bairro": "Tambaú",
        "telefone": "83 99999-0001", "disponibilidade": "Segundas e Quartas à tarde.", "observacao": "Foco em Terapia Cognitivo-Comportamental (TCC) para adultos.",
    },
    {
        "id": 2, "nome": "Mariana Costa - Psicologia", "categoria": "terapeuta", "especialidades": ["casal", "família", "relacionamentos"], "bairro": "Manaíra",
        "telefone": "83 99999-0002", "disponibilidade": "Terças e Quintas (manhã e tarde).", "observacao": "Especialista em terapia de casal e familiar.",
    },
    {
        "id": 3, "nome": "Ana Lima - Personal Trainer", "categoria": "personal_trainer", "especialidades": ["emagrecimento", "funcional", "corrida"], "bairro": "Cabo Branco",
        "telefone": "83 98888-0001", "disponibilidade": "Manhãs (6h às 10h).", "observacao": "Treinos na orla ou em academias parceiras.",
    },
    {
        "id": 4, "nome": "Ricardo Ferraz - Coach", "categoria": "personal_trainer", "especialidades": ["hipertrofia", "força", "musculação"], "bairro": "Manaíra",
        "telefone": "83 98888-0002", "disponibilidade": "Tardes e noites.", "observacao": "Especialista em ganho de massa muscular.",
    },
]

def popular_banco():
    db = SessionLocal()
    try:
        print("Iniciando a população do banco de dados...")
        for p_data in banco_de_dados_mvp:
            prestador_existente = db.query(Prestador).filter(Prestador.nome == p_data["nome"]).first()
            if not prestador_existente:
                novo_prestador = Prestador(
                    nome=p_data["nome"],
                    email=f'{p_data["nome"].lower().replace(" ", ".")}@conciergepro.com',
                    telefone=p_data.get("telefone"),
                    categoria=p_data["categoria"],
                    especialidades=p_data["especialidades"],
                    bairro=p_data["bairro"],
                    disponibilidade=p_data["disponibilidade"],
                    observacao=p_data["observacao"]
                )
                db.add(novo_prestador)
                print(f"Adicionado: {novo_prestador.nome}")
        db.commit()
        print("População do banco de dados concluída com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco()
