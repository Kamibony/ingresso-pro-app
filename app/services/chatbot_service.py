import os
import google.generativeai as genai
from ..database import SessionLocal
from ..models.database_models import Prestador
import json

# --- CONFIGURAÇÃO ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não definida no ambiente!")
genai.configure(api_key=GEMINI_API_KEY)

# --- ESTADO DA CONVERSA ---
chat_sessions = {}

# --- FERRAMENTAS DO GEMINI ---
def encontrar_prestador(categoria: str, especialidade: str = "", bairro: str = "") -> dict:
    """
    Busca prestadores de serviço no banco de dados com base nos filtros fornecidos.
    """
    print(f"--- [LOG FERRAMENTA] Ferramenta 'encontrar_prestador' foi chamada com: Categoria='{categoria}', Especialidade='{especialidade}', Bairro='{bairro}' ---")
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
            print("--- [LOG FERRAMENTA] Nenhum prestador encontrado no banco. ---")
            return {"info": "Não foram encontrados prestadores com os critérios especificados. Por favor, informe ao usuário e peça para tentar critérios diferentes."}

        resultados_dict = [{"id": p.id, "nome": p.nome, "especialidades": p.especialidades, "bairro": p.bairro} for p in resultados]
        print(f"--- [LOG FERRAMENTA] Encontrados {len(resultados_dict)} prestadores: {json.dumps(resultados_dict)} ---")
        return {"prestadores_encontrados": resultados_dict}
    finally:
        db.close()

# --- CÉREBRO PRINCIPAL DO GEMINI ---
system_instructions = """
Você é o "Concierge Pro", um assistente especialista em bem-estar.
Sua missão é conectar usuários a terapeutas e personal trainers em João Pessoa.
Seja sempre cordial, empático e muito prestativo.
Sempre use a ferramenta `encontrar_prestador` para buscar profissionais.
Antes de usar a ferramenta, se necessário, faça perguntas para qualificar a busca, como "Qual especialidade você procura?" ou "Tem preferência por algum bairro?".
Ao apresentar os resultados, formate-os de forma clara e sempre sugira um próximo passo, como "Gostaria de ver mais detalhes sobre algum deles?".
"""

all_tools = [encontrar_prestador]
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    tools=all_tools,
    system_instruction=system_instructions,
)

def processar_mensagem_chatbot(chat_id: str, user_message: str) -> str:
    print(f"--- [LOG CHATBOT] Iniciando processamento para chat_id {chat_id} ---")
    try:
        if chat_id not in chat_sessions:
            print(f"--- [LOG CHATBOT] Criando nova sessão de chat para {chat_id} ---")
            chat_sessions[chat_id] = model.start_chat(enable_automatic_function_calling=True)
        
        chat = chat_sessions[chat_id]
        print(f"--- [LOG CHATBOT] Enviando mensagem '{user_message}' para o modelo Gemini... ---")
        response = chat.send_message(user_message)
        
        # Log para ver o que o Gemini está tentando fazer
        print(f"--- [LOG CHATBOT] Resposta bruta do Gemini recebida. ---")
        
        response_text = response.text
        print(f"--- [LOG CHATBOT] Texto final da resposta: '{response_text}' ---")
        return response_text
    except Exception as e:
        print(f"!!! ERRO CRÍTICO NO PROCESSAMENTO DO CHATBOT: {e} !!!")
        return "Desculpe, ocorreu um problema com minha inteligência artificial. O engenheiro foi notificado."

