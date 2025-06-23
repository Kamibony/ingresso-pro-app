from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import chatbot_service

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.post("/test-chat", tags=["Testing"])
async def test_chat_endpoint(chat_message: ChatMessage):
    user_message = chat_message.message
    bot_response = chatbot_service.processar_mensagem_chatbot("test_session_id", user_message)
    return {"response": bot_response}

@router.get("/test-db-connection", tags=["Testing"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        db.execute(text('SELECT 1'))
        return {"status": "success", "message": "Conexão com o banco de dados bem-sucedida!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
