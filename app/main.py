from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env ANTES de tudo
load_dotenv()

# Agora podemos importar os outros módulos que usam as variáveis
from app.routers import event_router
from app.routers import session_router
from app.routers import testing_router # <-- 1. IMPORTA O ROUTER DE TESTE

app = FastAPI(
    title="Ingresso Pro API",
    description="API para gerenciamento de eventos e chatbot de ingressos.",
    version="1.0.0"
)

app.include_router(event_router.router)
app.include_router(session_router.router)
app.include_router(testing_router.router) # <-- 2. INCLUI O ROUTER DE TESTE

@app.get("/", tags=["Root"])
def read_root():
    return {"Project": "Ingresso Pro", "Status": "Up and Running"}
