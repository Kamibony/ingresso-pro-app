from pydantic import BaseModel, ConfigDict
import datetime

class Evento(BaseModel):
    # Adiciona a configuração para ignorar campos extras
    model_config = ConfigDict(extra='ignore')

    id: str | None = None # O ID será o nome do documento no Firestore
    nome: str
    descricao: str
    localizacao: str

class Sessao(BaseModel):
    # Adiciona a configuração para ignorar campos extras
    model_config = ConfigDict(extra='ignore')

    id: str | None = None # O ID será o nome do documento no Firestore
    evento_id: str
    data_hora_inicio: datetime.datetime
    capacidade: int
    vagas_disponiveis: int
    preco: float

class Reserva(BaseModel):
    # Adiciona a configuração para ignorar campos extras
    model_config = ConfigDict(extra='ignore')

    id: str | None = None
    sessao_id: str
    telegram_user_id: str
    nome_cliente: str
    quantidade_ingressos: int = 1
    status: str = "pendente" # Ex: pendente, pago, cancelado
    codigo_reserva: str
