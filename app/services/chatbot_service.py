import os
import google.generativeai as genai
from ..database import SessionLocal
from ..models.database_models import Prestador
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

chat_sessions = {}

def encontrar_prestador(categoria: str, especialidade: str = None, bairro: str = None) -> dict:
    print(f"--- Usando ferramenta 'encontrar_prestador' com Categoria='{categoria}' ---")
    db = SessionLocal()
    try:
        query = db.query(Prestador)
        if categoria:
            # Busca por 'terapeuta' ou 'personal_trainer' de forma flexível
            query = query.filter(Prestador.categoria.ilike(f"%{categoria.replace('_', ' ')}%"))
        if especialidade:
            query = query.filter(Prestador.especialidades.any(especialidade.lower()))
        if bairro:
            query = query.filter(Prestador.bairro.ilike(f"%{bairro}%"))
        
        resultados = query.limit(3).all()
        
        if not resultados:
            return {"info": "Não foram encontrados prestadores com os critérios especificados. Informe ao usuário e peça para tentar critérios diferentes."}

        resultados_dict = [{"id": p.id, "nome": p.nome, "especialidades": p.especialidades, "bairro": p.bairro} for p in resultados]
        return {"prestadores_encontrados": resultados_dict}
    finally:
        db.close()

system_instructions = """
Você é o 'Concierge Pro', um assistente prestativo.
Sua única função é usar a ferramenta `encontrar_prestador` para buscar terapeutas ou personal trainers.
NUNCA responda diretamente ao usuário sem usar a ferramenta.
Se a mensagem do usuário não tiver informações suficientes (categoria, especialidade, bairro), faça perguntas para obter os detalhes necessários para poder usar a ferramenta.
Seja direto. Se o usuário pedir "terapeuta", use a ferramenta com categoria="terapeuta". Se pedir "personal", use a ferramenta com categoria="personal_trainer".
"""

all_tools = [encontrar_prestador]
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    tools=all_tools,
    system_instruction=system_instructions,
)

def processar_mensagem_chatbot(chat_id: str, user_message: str) -> str:
    try:
        if chat_id not in chat_sessions:
            chat_sessions[chat_id] = model.start_chat(enable_automatic_function_calling=True)
        
        chat = chat_sessions[chat_id]
        response = chat.send_message(user_message)
        
        if not response.text:
            return "Não entendi o que você precisa. Você poderia especificar se busca por um terapeuta ou personal trainer?"
            
        return response.text
    except Exception as e:
        print(f"!!! ERRO CRÍTICO NO SERVIÇO DO CHATBOT: {e} !!!")
        return "Desculpe, ocorreu um problema com minha inteligência artificial."
