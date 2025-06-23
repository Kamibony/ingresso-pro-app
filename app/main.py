from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from .routers import telegram, dashboard, testing
from .models import database_models

app = FastAPI(title="Concierge Pro Platform")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Os routers que contêm a lógica da sua aplicação
app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/")
def read_root():
    return {"status": "API online e pronta para servir!"}
