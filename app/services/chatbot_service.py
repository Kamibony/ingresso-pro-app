import os
import google.generativeai as genai
from ..database import SessionLocal
from ..models.database_models import Prestador

# --- CONFIGURAÇÃO ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não definida no ambiente!")
genai.configure(api_key=GEMINI_API_KEY)


# --- ESTADO DA CONVERSA (Em memória, mas separado por usuário) ---
chat_sessions = {}


# --- FERRAMENTAS DO GEMINI QUE ACESSAM O BANCO DE DADOS ---
def encontrar_prestador(categoria: str, especialidade: str = "", bairro: str = "") -> dict:
    """
    Busca prestadores de serviço no banco de dados com base nos filtros fornecidos.
    Retorna uma lista de até 3 profissionais qualificados.
    """
    print(f"--- Ferramenta: Buscando no DB: {categoria} com esp: '{especialidade}' no bairro '{bairro}' ---")
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
            return {"error": f"Desculpe, não encontrei prestadores com os critérios informados. Tente uma busca mais ampla."}

        resultados_dict = [
            {
                "id": p.id,
                "nome": p.nome,
                "especialidades": p.especialidades,
                "bairro": p.bairro,
                "disponibilidade": p.disponibilidade,
                "observacao": p.observacao
            }
            for p in resultados
        ]
        return {"prestadores_encontrados": resultados_dict}
    except Exception as e:
        print(f"!!! ERRO NA FERRAMENTA DE BUSCA: {e} !!!")
        return {"error": "Ocorreu um erro interno ao buscar no banco de dados."}
    finally:
        db.close()


# --- CÉREBRO PRINCIPAL DO GEMINI ---
system_instructions = """
Você é o "Concierge Pro", um assistente virtual especialista em bem-estar.
Sua missão é conectar usuários a terapeutas e personal trainers qualificados em João Pessoa.
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
    """
    Função central que gerencia a conversa do usuário e retorna a resposta da IA.
    Mantém o histórico de conversas separado por chat_id.
    """
    try:
        if chat_id not in chat_sessions:
            print(f"Iniciando nova sessão de chat para o ID: {chat_id}")
            chat_sessions[chat_id] = model.start_chat(enable_automatic_function_calling=True)
        
        chat = chat_sessions[chat_id]
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        print(f"!!! ERRO NO SERVIÇO DO GEMINI: {e} !!!")
        return "Desculpe, meu cérebro de IA encontrou um problema. Poderia tentar reformular sua pergunta?"
