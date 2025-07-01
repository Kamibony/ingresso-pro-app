from app.database import db
from app.models.pydantic_models import Sessao
from typing import List
import datetime

def criar_sessao(evento_id: str, sessao: Sessao) -> Sessao:
    """
    Cria uma nova sessão como uma sub-coleção de um evento específico.
    """
    try:
        # Pega a referência da sub-coleção 'sessoes' dentro do evento específico
        sessoes_ref = db.collection('eventos').document(evento_id).collection('sessoes')

        # Adiciona um novo documento de sessão
        sessao.evento_id = evento_id
        sessao_data = sessao.model_dump(exclude={'id'})
        update_time, doc_ref = sessoes_ref.add(sessao_data)

        # Retorna a sessão com seu novo ID
        sessao.id = doc_ref.id
        print(f"Sessão para o evento {evento_id} criada com ID: {sessao.id}")
        return sessao
    except Exception as e:
        print(f"Erro ao criar sessão: {e}")
        raise

def listar_sessoes_por_evento(evento_id: str) -> List[Sessao]:
    """
    Lista todas as sessões de um evento específico.
    """
    try:
        sessoes_ref = db.collection('eventos').document(evento_id).collection('sessoes')
        docs = sessoes_ref.order_by('data_hora_inicio').stream()

        sessoes = []
        for doc in docs:
            sessao_data = doc.to_dict()
            sessao_data['id'] = doc.id
            sessoes.append(Sessao(**sessao_data))
        
        print(f"Encontradas {len(sessoes)} sessões para o evento {evento_id}.")
        return sessoes
    except Exception as e:
        print(f"Erro ao listar sessões: {e}")
        raise
