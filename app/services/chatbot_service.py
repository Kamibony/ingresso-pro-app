import os
import google.generativeai as genai
from typing import List
# A importação correta, baseada no uso de outras partes da biblioteca
from google.generativeai.protos import Part

# Importa nossos serviços de dados
from app.services import event_service

# --- Configurações da API do Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida.")
genai.configure(api_key=GEMINI_API_KEY)

# --- Ferramentas para o Gemini ---
def procurar_eventos_disponiveis() -> List[dict]:
    """Busca no banco de dados por todos os eventos disponíveis."""
    print("--- [Tool Call] Executando: procurar_eventos_disponiveis ---")
    try:
        eventos = event_service.listar_eventos()
        if not eventos:
            return [{"info": "Nenhum evento encontrado no momento."}]
        return [evento.model_dump() for evento in eventos]
    except Exception as e:
        print(f"Erro na ferramenta 'procurar_eventos_disponiveis': {e}")
        return [{"erro": "Ocorreu um erro ao buscar os eventos."}]

# --- Lógica Principal do Chatbot ---
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[procurar_eventos_disponiveis]
)

def generate_response(session_id: str, message: str) -> str:
    """Gera uma resposta do chatbot para uma mensagem do usuário."""
    print(f"--- [Chat] Recebida nova mensagem de '{session_id}': '{message}' ---")
    chat_session = model.start_chat()
    response = chat_session.send_message(message)
    
    answer = ""
    try:
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            tool_response_data = procurar_eventos_disponiveis()
            
            # Envia a resposta da ferramenta de volta para o Gemini
            final_response = chat_session.send_message(
                Part(
                    function_response=genai.protos.FunctionResponse(
                        name=function_call.name,
                        response={"result": tool_response_data},
                    )
                ),
            )
            answer = final_response.text
        else:
            answer = response.text

    except Exception as e:
        print(f"--- [ERRO] Erro ao processar a resposta do Gemini: {e} ---")
        answer = "Desculpe, tive um problema para processar sua solicitação. Tente novamente."

    print(f"--- [Chat] Resposta gerada: '{answer}' ---")
    return answer
