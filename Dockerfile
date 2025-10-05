# Usar uma imagem oficial do Python
FROM python:3.11-slim

# Criar diretório da aplicação
WORKDIR /app

# Copiar dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o projeto
COPY . .

# Variável de ambiente (ajuste se quiser)
ENV PORT=8000

# Comando para iniciar FastAPI no Render
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
