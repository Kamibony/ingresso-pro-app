# Concierge Pro - Plataforma de Serviços Inteligente

## Descrição
Aplicação web e chatbot para conectar usuários a prestadores de serviço qualificados, com implantação automatizada no Google Cloud Run.

## Setup do Projeto

1.  **Ambiente Virtual:**
    python -m venv venv
    .\venv\Scripts\Activate.ps1

2.  **Variáveis de Ambiente:**
    - Se o arquivo .env não existir, renomeie o .env.example para .env.
    - Preencha todas as chaves de API necessárias.

3.  **Instalar Dependências:**
    pip install -r requirements.txt

4.  **Criar e Popular o Banco de Dados (executar apenas uma vez):**
    - Primeiro, inicie o servidor com uvicorn app.main:app --reload para criar as tabelas e pare com Ctrl + C.
    - Depois, rode python create_first_provider.py para adicionar os dados iniciais.

## Executando a Aplicação Localmente

1.  **Iniciar o Servidor:**
    uvicorn app.main:app --reload

2.  **Acessar os Endpoints:**
    - Saúde do Servidor: http://127.0.0.1:8000/
    - Painel do Prestador (Exemplo): http://127.0.0.1:8000/dashboard/1

## Deploy Automático
Qualquer git push no branch main irá acionar o gatilho no Google Cloud Build, que automaticamente construirá e implantará a nova versão no Cloud Run.
Versão 1.0 no ar!AGORA VAI!
Re-executando o build Fri Jun 20 11:58:23 PM UTC 2025 após correção de permissões.
## Forçando a atualização final - Sat Jun 21 04:47:25 PM UTC 2025
