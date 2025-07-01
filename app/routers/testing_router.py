from fastapi import APIRouter
from pydantic import BaseModel
from app.services import chatbot_service

router = APIRouter()

class TestMessage(BaseModel):
    session_id: str = "test_session"
    message: str

@router.post("/test-chat/", tags=["Testes do Chatbot"])
def endpoint_test_chat(request: TestMessage):
    """
    Endpoint para enviar uma mensagem de teste para o chatbot e receber a resposta.
    """
    response_text = chatbot_service.generate_response(
        session_id=request.session_id,
        message=request.message
    )
    return {"response": response_text}
