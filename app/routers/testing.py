# -*- coding: utf-8 -*-
from fastapi import APIRouter
from pydantic import BaseModel
from ..services import chatbot_service

router = APIRouter()
class ChatMessage(BaseModel):
    message: str

@router.post("/test-chat")
async def test_chat_endpoint(chat_message: ChatMessage):
    user_message = chat_message.message
    bot_response = chatbot_service.processar_mensagem_chatbot(user_message)
    return {"response": bot_response}
