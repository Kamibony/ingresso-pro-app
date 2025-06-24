# Etapa 1: Use uma imagem Python oficial e leve
FROM python:3.10-slim as builder

# Define o diretório de trabalho
WORKDIR /app

# Instala o poetry (se você usar, senão, pode remover) e as dependências
# Usar o pip install direto também funciona
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Etapa 2: Copia os arquivos da aplicação
FROM python:3.10-slim

WORKDIR /app

# Copia as dependências instaladas da etapa anterior
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copia TODOS os arquivos da sua aplicação para o diretório de trabalho
# Esta é a linha mais importante para resolver o problema atual
COPY . .

# Expõe a porta que o Cloud Run usará
EXPOSE 8080

# Comando para iniciar a aplicação usando uvicorn
# O Cloud Run injetará a variável de ambiente PORT.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
