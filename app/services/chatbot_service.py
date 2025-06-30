import os
import google.generativeai as genai
import googlemaps
from sqlalchemy.orm import Session
from app.models.database_models import ChatHistory, Prestador

# --- Configurações das APIs ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Variável de ambiente GEMINI_API_KEY não foi definida.")
genai.configure(api_key=GEMINI_API_KEY)

PLACES_API_KEY = os.getenv("PLACES_API_KEY")
if not PLACES_API_KEY:
    raise ValueError("Variável de ambiente PLACES_API_KEY não foi definida.")
gmaps = googlemaps.Client(key=PLACES_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# --- Definição das Ferramentas (Tools) ---


def encontrar_prestador_tool(especialidade: str) -> dict:
    """Busca em nossa base de dados exclusiva por profissionais VERIFICADOS, como Terapeutas e Personal Trainers."""
    pass


def pesquisar_locais_no_maps(query: str) -> dict:
    """Pesquisa por estabelecimentos e profissionais em uma busca pública no Google Maps. Use para buscas genéricas."""
    pass


# --- Funções de Execução das Ferramentas ---


def encontrar_prestador_na_base(especialidade: str, db: Session) -> dict:
    """Executa a busca real de prestadores de serviço VERIFICADOS no banco de dados."""
    print(f"[Tool Call - Interna] Buscando prestador: {especialidade}")
    try:
        query = db.query(Prestador).filter(
            Prestador.is_verified == True,
            Prestador.especialidades.ilike(f"%{especialidade}%"),
        )
        prestadores = query.all()
        if not prestadores:
            return {
                "status": "Não encontrado",
                "message": "Nenhum prestador verificado foi encontrado na nossa base de dados.",
            }

        resultados = [f"- {p.nome} (Telefone: {p.telefone})" for p in prestadores]
        return {"status": "Sucesso", "prestadores": "\n".join(resultados)}
    except Exception as e:
        print(f"[Tool Error - Interna] {e}")
        return {
            "status": "Erro",
            "message": "Ocorreu um erro ao buscar na nossa base de dados.",
        }


def executar_pesquisa_places(query: str) -> dict:
    """Executa a busca real usando a Places API do Google Maps."""
    print(f"[Tool Call - Externa] Buscando no Google Maps: {query}")
    try:
        places_result = gmaps.places(
            query=f"{query} em João Pessoa", region="br", language="pt-BR"
        )
        if places_result.get("status") == "OK" and places_result.get("results"):
            resultados = []
            for place in places_result["results"][:3]:
                name = place.get("name")
                address = place.get("formatted_address", "Endereço não disponível")
                resultados.append(f"- {name} (Endereço: {address})")
            return {"status": "Sucesso", "locais": "\n".join(resultados)}
        else:
            return {
                "status": "Não encontrado",
                "message": "Nenhum local correspondente foi encontrado na busca pública.",
            }
    except Exception as e:
        print(f"[Tool Error - Externa] {e}")
        return {
            "status": "Erro",
            "message": "Ocorreu um erro ao fazer a busca pública.",
        }


# --- Lógica Principal do Chatbot ---


def generate_response(session_id: str, message: str, db: Session) -> str:
    """
    Gera uma resposta do chatbot, mantendo o histórico da conversa.
    """
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.timestamp.asc())
        .all()
    )

    chat_history_for_model = []
    for entry in history:
        chat_history_for_model.append({"role": "user", "parts": [entry.message]})
        chat_history_for_model.append({"role": "model", "parts": [entry.response]})

    tools_map = {
        "encontrar_prestador_tool": lambda especialidade: encontrar_prestador_na_base(
            especialidade, db
        ),
        "pesquisar_locais_no_maps": executar_pesquisa_places,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""Você é o Concierge Pro, um assistente virtual amigável, prestativo e com ótima memória. Sua especialidade é encontrar prestadores de serviço qualificados, como terapeutas e personal trainers.

**Sua Personalidade:**
- Mantenha um tom de conversa natural e contínuo.
- Lembre-se do que o usuário disse nas mensagens anteriores para entender o contexto de novas perguntas.
- Se o usuário pedir por uma busca e depois mencionar apenas um novo bairro (ex: "E em Manaíra?"), entenda que ele ainda está procurando pelo mesmo tipo de serviço.
- Se o usuário agradecer, responda de forma gentil e pergunte se há algo mais em que possa ajudar.

**Regras de Execução de Ferramentas:**
1.  Sua prioridade MÁXIMA é usar a ferramenta `encontrar_prestador_tool` para buscar em nossa base de dados de parceiros VERIFICADOS.
2.  Se a ferramenta `encontrar_prestador_tool` retornar um status de "Não encontrado", e somente neste caso, use a ferramenta `pesquisar_locais_no_maps` para fazer uma busca pública.
3.  SEMPRE seja transparente sobre a origem da informação.
    - Se a ferramenta `encontrar_prestador_tool` encontrou resultados, diga: "Encontrei os seguintes profissionais verificados em nossa plataforma para você: [resultado]".
    - Se a ferramenta `pesquisar_locais_no_maps` encontrou resultados, diga: "Não encontrei um parceiro verificado, mas em uma busca pública, encontrei estes locais para você: [resultado]".
""",
        tools=[encontrar_prestador_tool, pesquisar_locais_no_maps],
    )

    chat_session = model.start_chat(history=chat_history_for_model)
    response = chat_session.send_message(message)

    try:
        # Loop para lidar com chamadas de função, se houver
        while response.candidates[0].content.parts[0].function_call.name:
            function_call = response.candidates[0].content.parts[0].function_call
            tool_name = function_call.name
            tool_args = dict(function_call.args)

            if tool_name in tools_map:
                function_to_call = tools_map[tool_name]
                tool_response = function_to_call(**tool_args)

                if (
                    isinstance(tool_response, dict)
                    and tool_response.get("status") == "Sucesso"
                ):
                    if "prestadores" in tool_response:
                        formatted_content = tool_response["prestadores"]
                    elif "locais" in tool_response:
                        formatted_content = tool_response["locais"]
                    else:
                        formatted_content = "Ação concluída com sucesso."
                else:
                    formatted_content = str(tool_response)

                response = chat_session.send_message(
                    genai.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=tool_name,
                            response={"content": formatted_content},
                        )
                    )
                )
            else:
                break
    except (AttributeError, IndexError):
        pass

    response_text = response.text

    new_entry = ChatHistory(
        session_id=session_id, message=message, response=response_text
    )
    db.add(new_entry)
    db.commit()

    return response_text
