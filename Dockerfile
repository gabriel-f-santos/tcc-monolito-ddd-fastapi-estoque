FROM python:3.13.0-slim-bookworm

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Diretório de trabalho
WORKDIR /app

# Instalar dependências de sistema necessárias
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar apenas o código-fonte da aplicação
COPY src/ ./src
COPY scripts/ ./scripts
COPY alembic/ ./alembic
COPY alembic.ini .
COPY .env.example .env

# Copiar e marcar o entrypoint como executável ANTES de mudar para usuário não-root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Criar usuário não-root e ajustar permissões do /app
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

# Agora sim, troca para o usuário 'app'
USER app

# Expor porta do FastAPI
EXPOSE 8080

# Healthcheck
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8080/api/v1/health/ || exit 1

# A porta 80 fica exposta também (se necessário)
EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
