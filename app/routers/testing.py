from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.get("/test-db-connection", tags=["Testing"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Tenta executar uma consulta simples
        db.execute('SELECT 1')
        return {"status": "success", "message": "Conexão com o banco de dados bem-sucedida!"}
    except Exception as e:
        return {"status": "error", "message": "Falha na conexão com o banco de dados.", "error_details": str(e)}
