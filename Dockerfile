# Estágio 1: Builder - Usamos uma imagem Python leve para instalar as dependências
FROM python:3.11-slim as builder

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia apenas o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Estágio 2: Final - A imagem limpa que rodará na nuvem
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia as dependências já instaladas do estágio "builder"
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copia o código da nossa aplicação (a pasta 'app') para dentro do contêiner
COPY ./app /app

# Expõe a porta que o Uvicorn usará, padrão para o Cloud Run
EXPOSE 8080

# O comando que será executado quando o contêiner iniciar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
