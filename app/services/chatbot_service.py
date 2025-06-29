import os
import google.generativeai as genai
from sqlalchemy.orm import Session

from ..models.database_models import Prestador, ChatHistory

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Configuração do modelo e das ferramentas
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def encontrar_prestador(db: Session, especialidade: str, cidade: str) -> list[dict]:
    """
    Consulta o banco de dados para encontrar prestadores de serviço
    com base na especialidade e cidade.
    """
    query = db.query(Prestador)
    if especialidade:
        query = query.filter(Prestador.especialidade.ilike(f"%{especialidade}%"))
    if cidade:
        query = query.filter(Prestador.cidade.ilike(f"%{cidade}%"))
    
    results = query.all()
    if not results:
        return [{"info": "Nenhum prestador encontrado com esses critérios."}]
    
    return [
        {
            "nome": p.nome,
            "especialidade": p.especialidade,
            "cidade": p.cidade,
            "bairro": p.bairro,
            "telefone": p.telefone,
            "bio": p.bio
        } for p in results
    ]

# Cria um wrapper para a função da ferramenta, passando a sessão do DB
def get_tools(db: Session):
    def find_provider_tool(especialidade: str, cidade: str):
        return encontrar_prestador(db, especialidade, cidade)

    tools = {
        "encontrar_prestador": find_provider_tool
    }
    return tools

# Inicia o modelo generativo
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Você é um concierge virtual chamado 'Concierge Pro'. Sua função é ajudar usuários a encontrar terapeutas e personal trainers qualificados. Seja sempre cordial e prestativo. Use a ferramenta `encontrar_prestador` para buscar no banco de dados. Peça a especialidade e a cidade do usuário se não forem fornecidas. Confirme as informações antes de buscar. Nunca invente prestadores ou informações. Se não encontrar ninguém, informe o usuário claramente.",
)

def generate_response(session_id: str, message: str, db: Session) -> str:
    """
    Gera uma resposta do chatbot, mantendo o histórico da conversa.
    """
    # Recupera histórico da conversa do banco de dados
    history = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp.asc()).all()
    
    # Formata o histórico para o modelo Gemini
    chat_history_for_model = []
    for entry in history:
        chat_history_for_model.append({"role": "user", "parts": [entry.message]})
        chat_history_for_model.append({"role": "model", "parts": [entry.response]})

    # Inicia a sessão de chat com o histórico
    chat_session = model.start_chat(
        history=chat_history_for_model,
        enable_automatic_function_calling=True,
    )

    # Envia a nova mensagem e obtém a resposta
    response = chat_session.send_message(message)
    response_text = response.text

    # Salva a nova interação no banco de dados
    new_entry = ChatHistory(
        session_id=session_id,
        message=message,
        response=response_text
    )
    db.add(new_entry)
    db.commit()

    return response_text
