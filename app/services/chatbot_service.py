# app/services/chatbot_service.py (Versão Final com Chaves Separadas)
# -*- coding: utf-8 -*-
import os
import google.generativeai as genai
import googlemaps
import requests
from datetime import datetime

# --- CONFIGURAÇÃO DAS APIS COM CHAVES SEPARADAS ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
Maps_API_KEY = os.getenv("Maps_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
gmaps = googlemaps.Client(key=Maps_API_KEY)

# --- BANCO DE DADOS EM MEMÓRIA (MVP) ---
banco_de_dados_mvp = [
    {
        "id": 1,
        "nome": "Dr. Carlos Andrade",
        "categoria": "terapeuta",
        "especialidades": ["ansiedade", "depressão", "TCC"],
        "bairro": "Tambaú",
        "disponibilidade": "Segundas e Quartas à tarde.",
        "contato": "83 99999-0001",
        "observacao": "Foco em Terapia Cognitivo-Comportamental (TCC) para adultos.",
    },
    {
        "id": 2,
        "nome": "Mariana Costa - Psicologia",
        "categoria": "terapeuta",
        "especialidades": ["casal", "família", "relacionamentos"],
        "bairro": "Manaíra",
        "disponibilidade": "Terças e Quintas (manhã e tarde).",
        "contato": "83 99999-0002",
        "observacao": "Especialista em terapia de casal e familiar.",
    },
    {
        "id": 3,
        "nome": "Ana Lima - Personal Trainer",
        "categoria": "personal_trainer",
        "especialidades": ["emagrecimento", "funcional", "corrida"],
        "bairro": "Cabo Branco",
        "disponibilidade": "Manhãs (6h às 10h).",
        "contato": "83 98888-0001",
        "observacao": "Treinos na orla ou em academias parceiras.",
    },
    {
        "id": 4,
        "nome": "Ricardo Ferraz - Coach",
        "categoria": "personal_trainer",
        "especialidades": ["hipertrofia", "força", "musculação"],
        "bairro": "Manaíra",
        "disponibilidade": "Tardes e noites.",
        "contato": "83 98888-0002",
        "observacao": "Especialista em ganho de massa muscular.",
    },
]
chat_session_state = {"last_results": []}


# --- FERRAMENTAS ---
def encontrar_prestador(
    categoria: str, especialidade: str = "", bairro: str = ""
) -> dict:
    print(
        f"--- Ferramenta: Buscando {categoria} com especialidade '{especialidade}' no bairro '{bairro}' ---"
    )
    resultados = [p for p in banco_de_dados_mvp if p["categoria"] == categoria]
    if especialidade:
        resultados = [
            p
            for p in resultados
            if especialidade.lower() in [e.lower() for e in p["especialidades"]]
        ]
    if bairro:
        resultados = [p for p in resultados if bairro.lower() == p["bairro"].lower()]
    if not resultados:
        return {"error": f"Não encontrei prestadores com esses critérios."}
    chat_session_state["last_results"] = resultados[:3]
    return {"prestadores": resultados[:3]}


def obter_rota_para_local(destino: str, origem: str) -> dict:
    print(f"--- Ferramenta: Calculando rota de '{origem}' para '{destino}' ---")
    try:
        directions_result = gmaps.directions(
            origem, destino, mode="driving", language="pt-BR"
        )
        if not directions_result:
            return {"error": "Não foi possível calcular a rota."}
        rota = directions_result[0]["legs"][0]
        return {
            "rota": {
                "distancia": rota["distance"]["text"],
                "duracao": rota["duration"]["text"],
            }
        }
    except Exception as e:
        print(f"!!! ERRO NA API DE MAPAS: {e} !!!")
        return {"error": "Ocorreu um erro ao consultar a API de Rotas."}


def obter_previsao_tempo(cidade: str) -> dict:
    print(f"--- Ferramenta: Verificando o tempo em '{cidade}' ---")
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={OPENWEATHER_API_KEY}&q={cidade}&units=metric&lang=pt_br"
    response = requests.get(url)
    data = response.json()
    if data.get("cod") != 200:
        return {"error": f"Não encontrei o tempo para '{cidade}'."}
    main, weather = data["main"], data["weather"][0]
    return {
        "previsao": {
            "cidade": data["name"],
            "temperatura": f"{main['temp']}°C",
            "descricao": weather["description"],
        }
    }


# --- CÉREBRO DO GEMINI ---
system_instructions = """
Você é o "Concierge de Bem-Estar", um assistente especialista.

REGRAS:
1.  **TRIAGEM:** Se o usuário buscar "terapeuta" ou "personal_trainer", faça uma pergunta de qualificação sobre a especialidade ou objetivo antes de chamar a ferramenta `encontrar_prestador`.
2.  **ROTAS:** Para `obter_rota_para_local`, a origem é obrigatória. Se o usuário não fornecer, pergunte "De onde você está saindo?". Se ele responder algo genérico como "daqui", explique que precisa de um endereço ou CEP.
3.  **CONTEXTO:** Use a memória `last_results` para entender referências como "o primeiro" ou "a opção 2".
4.  **AÇÕES:** Sempre sugira próximos passos.
"""
all_tools = [encontrar_prestador, obter_rota_para_local, obter_previsao_tempo]
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    tools=all_tools,
    system_instruction=system_instructions,
)
chat = model.start_chat(enable_automatic_function_calling=True)


def processar_mensagem_chatbot(user_message: str) -> str:
    """Função central que recebe a mensagem e retorna a resposta da IA."""
    try:
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        # Este print é crucial para a depuração
        print(f"!!! ERRO NO SERVIÇO DO GEMINI: {e} !!!")
        return "Desculpe, estou com um problema interno na comunicação com a IA. Tente novamente."
