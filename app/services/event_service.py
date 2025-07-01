from app.database import db
from app.models.pydantic_models import Evento
from typing import List
from pydantic import ValidationError

def criar_evento(evento: Evento) -> Evento:
    """
    Cria um novo documento de evento na coleção 'eventos' do Firestore.
    """
    try:
        eventos_ref = db.collection('eventos')
        evento_data = evento.model_dump(exclude={'id'})
        update_time, doc_ref = eventos_ref.add(evento_data)
        evento.id = doc_ref.id
        print(f"Evento '{evento.nome}' criado com ID: {evento.id}")
        return evento
    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        raise

def listar_eventos() -> List[Evento]:
    """
    Lista todos os eventos da coleção 'eventos' do Firestore.
    """
    print("--- [DEBUG] Executando a função 'listar_eventos'... ---")
    try:
        eventos_ref = db.collection('eventos')
        docs = eventos_ref.stream()

        eventos = []
        document_count = 0
        for doc in docs:
            document_count += 1
            print(f"\n[DEBUG] Processando documento. ID: {doc.id}")
            evento_data = doc.to_dict()
            print(f"[DEBUG] Dados brutos do Firestore: {evento_data}")
            
            try:
                # Adiciona o ID do documento ao dicionário para validação do Pydantic
                evento_data['id'] = doc.id
                print("[DEBUG] Tentando converter para o modelo Pydantic 'Evento'...")
                evento_obj = Evento(**evento_data)
                eventos.append(evento_obj)
                print("[DEBUG] SUCESSO! Evento adicionado à lista.")
            except ValidationError as e:
                print(f"[DEBUG] ERRO DE VALIDAÇÃO DO PYDANTIC: O documento com ID {doc.id} é inválido.")
                print(e)
            except Exception as e:
                print(f"[DEBUG] Ocorreu um erro inesperado ao processar o documento {doc.id}: {e}")

        print(f"\n--- [DEBUG] Fim do loop. Total de documentos encontrados no Firestore: {document_count} ---")
        print(f"--- [DEBUG] Total de eventos validados e retornados: {len(eventos)} ---")
        return eventos
    except Exception as e:
        print(f"--- [DEBUG] ERRO GERAL na função 'listar_eventos': {e} ---")
        raise
