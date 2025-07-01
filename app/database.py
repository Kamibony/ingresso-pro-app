from google.cloud import firestore
import os

# Pega o ID do projeto a partir das variáveis de ambiente
# (Você precisará adicionar GOOGLE_CLOUD_PROJECT ao seu arquivo .env)
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

if not project_id:
    raise ValueError("A variável de ambiente GOOGLE_CLOUD_PROJECT não foi definida!")

# Instancia o cliente do Firestore, especificando o projeto.
# A biblioteca usará automaticamente as credenciais que
# você configurou com 'gcloud auth application-default login'.
db = firestore.Client(project=project_id)

print(f"✅ Cliente Firestore inicializado para o projeto: {db.project}")
