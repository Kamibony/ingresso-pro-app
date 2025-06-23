# --- Estágio 1: Builder ---
# Usamos um 'apelido' "builder" para este estágio.
FROM python:3.12-slim as builder

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Instala as dependências de build do sistema (se necessário)
# Para psycopg2, às vezes é necessário o build-essential e libpq-dev
# RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copia apenas o arquivo de requisitos primeiro para aproveitar o cache do Docker.
COPY requirements.txt .

# Instala as dependências.
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# --- Estágio 2: Runtime ---
# Esta é a imagem final, que será muito menor.
FROM python:3.12-slim

# Define o diretório de trabalho.
WORKDIR /app

# Copia as dependências pré-compiladas do estágio 'builder'.
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Instala as dependências a partir dos arquivos locais, o que é muito mais rápido.
RUN pip install --no-cache /wheels/*

# Copia todo o código da sua aplicação para o contêiner.
# O primeiro 'app' é a sua pasta local, o segundo é o destino dentro do contêiner.
COPY ./app /app/app

# Expõe a porta que o Cloud Run usará.
EXPOSE 8080

# --- O COMANDO FINAL E CORRIGIDO ---
# Inicia o servidor Uvicorn ouvindo em todas as interfaces de rede na porta 8080.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
