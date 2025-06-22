from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

class ChatMessage(BaseModel):
    message: str

@router.post("/test-chat", tags=["Testing"])
async def test_chat_endpoint(chat_message: ChatMessage):
    user_message = chat_message.message
    bot_response = chatbot_service.get_response("test_session", user_message)
    return {"response": bot_response}

@router.get("/test-db-connection", tags=["Testing"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute('SELECT 1')
        return {"status": "success", "message": "Conexão com o banco de dados bem-sucedida!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
