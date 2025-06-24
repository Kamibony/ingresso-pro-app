import os
import google.generativeai as genai
from ..database import SessionLocal
from ..models.database_models import Prestador
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

chat_sessions = {}

def encontrar_prestador(categoria: str, especialidade: str = "", bairro: str = "") -> dict:
    print(f"--- PASSO 6: Ferramenta 'encontrar_prestador' CHAMADA! Buscando: Cat='{categoria}', Esp='{especialidade}', Bairro='{bairro}' ---")
    db = SessionLocal()
    try:
        query = db.query(Prestador)
        if categoria:
            query = query.filter(Prestador.categoria.ilike(f"%{categoria}%"))
        if especialidade:
            query = query.filter(Prestador.especialidades.any(especialidade.lower()))
        if bairro:
            query = query.filter(Prestador.bairro.ilike(f"%{bairro}%"))
        
        resultados = query.limit(3).all()
        
        if not resultados:
            print("--- [FERRAMENTA] Nenhum prestador encontrado. ---")
            return {"info": "Não foram encontrados prestadores com os critérios especificados. Informe ao usuário e peça para tentar critérios diferentes."}

        resultados_dict = [{"id": p.id, "nome": p.nome} for p in resultados]
        print(f"--- [FERRAMENTA] Encontrados {len(resultados_dict)} prestadores. ---")
        return {"prestadores_encontrados": resultados_dict}
    finally:
        db.close()

system_instructions = "Você é o 'Concierge Pro', um assistente especialista em bem-estar. Sua missão é conectar usuários a terapeutas e personal trainers em João Pessoa. Use as ferramentas para encontrar profissionais. Seja cordial e prestativo."

all_tools = [encontrar_prestador]
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    tools=all_tools,
    system_instruction=system_instructions,
)

def processar_mensagem_chatbot(chat_id: str, user_message: str) -> str:
    print(f"--- PASSO 5: Função 'processar_mensagem_chatbot' ACIONADA com a mensagem: '{user_message}' ---")
    try:
        if chat_id not in chat_sessions:
            chat_sessions[chat_id] = model.start_chat(enable_automatic_function_calling=True)
        
        chat = chat_sessions[chat_id]
        response = chat.send_message(user_message)
        
        # Este log nos dirá se o Gemini tentou chamar a ferramenta
        print(f"--- PASSO 7: Resposta bruta do Gemini: {response} ---")
        
        response_text = response.text
        return response_text
    except Exception as e:
        print(f"!!! ERRO CRÍTICO NO SERVIÇO DO CHATBOT: {e} !!!")
        return "Desculpe, ocorreu um problema com a minha inteligência artificial."
