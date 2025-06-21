# Fase 1: Builder - Instala as dependências
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fase 2: Final - Monta a imagem final enxuta
FROM python:3.11-slim
WORKDIR /app
# --- A CORREÇÃO ---
# Copia as bibliotecas E os executáveis da fase de build
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
# Copia o código da sua aplicação
COPY ./app /app
# Expõe a porta que o Cloud Run usará
EXPOSE 8080
# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
